import json, os, datetime as dt
from flask import Blueprint, request, render_template, send_from_directory
from ..client import search_companies, get_company_sfdr, DatalandError
from ..services.util import safe_filename

bp = Blueprint("sfdr", __name__, url_prefix="/sfdr")

@bp.get("/")
def form():
    return render_template("sfdr.html", candidates=None)

@bp.post("/fetch")
def fetch():
    name = (request.form.get("name") or "").strip()
    period_raw = (request.form.get("period") or "").strip()
    active = request.form.get("active") is not None
    selected_id = (request.form.get("company_id") or "").strip() or None

    candidates = []
    filepath = filename = preview = None
    status = None; message = ""

    try:
        candidates = search_companies(name, limit=100)
        if not candidates:
            raise DatalandError("Keine Treffer gefunden.")
        if not selected_id:
            return render_template("sfdr.html", candidates=candidates[:50], name=name, period=period_raw, active=active,
                                   info="Bitte Eintrag wählen und erneut senden.")
        period = None
        if period_raw:
            try:
                period = int(period_raw)
            except ValueError:
                period = None
        data = get_company_sfdr(selected_id, reporting_period=period, show_only_active=active)
        safe = safe_filename(next((c.company_name for c in candidates if c.company_id == selected_id), "company"), "company")
        tag = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        p = f"{period}" if period is not None else "all"
        a = "active" if active else "all"
        filename = f"sfdr_{safe}_{p}_{a}_{tag}.json"
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        preview = json.dumps(data, ensure_ascii=False, indent=2)
        if len(preview) > 2000:
            preview = preview[:2000] + "\n… (gekürzt)"
        status = "ok"; message = "JSON gespeichert."
    except DatalandError as e:
        status = "err"; message = str(e)
    except Exception as e:
        status = "err"; message = f"Unerwarteter Fehler: {e}"

    return render_template("sfdr.html", candidates=candidates[:50] if candidates else None, name=name,
                           period=period_raw, active=active, selected_id=selected_id, status=status, message=message,
                           filename=filename, filepath=filepath, preview=preview)

@bp.get("/download/<path:fname>")
def download(fname: str):
    return send_from_directory(os.getcwd(), fname, as_attachment=True)
