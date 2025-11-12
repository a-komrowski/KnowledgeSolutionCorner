from flask import Blueprint, request, render_template
from ..client import search_companies, DatalandError
from flask import jsonify

bp = Blueprint("companies", __name__, url_prefix="/companies")

@bp.get("/")
def form():
    return render_template("companies.html", candidates=None, name="")

@bp.post("/search")
def do_search():
    name = (request.form.get("name") or "").strip()
    try:
        candidates = search_companies(name, limit=100)
        return render_template("companies.html", candidates=candidates[:50], name=name)
    except DatalandError as e:
        return render_template("companies.html", candidates=None, name=name, error=str(e))

@bp.get("/api/search")
def api_search():
    """
    JSON-Suche für Live-Dropdowns:
    GET /companies/api/search?name=Siemens&limit=50
    """
    name = (request.args.get("name") or "").strip()
    limit = int(request.args.get("limit") or 50)
    try:
        results = search_companies(name, limit=limit)
        return jsonify([{"companyId": c.company_id, "companyName": c.company_name} for c in results])
    except DatalandError as e:
        return jsonify({"error": str(e)}), 502
