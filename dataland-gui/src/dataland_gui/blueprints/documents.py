from flask import Blueprint, request, render_template, Response, abort, request as flask_request
from ..client import search_companies, list_documents, stream_document, DatalandError
from ..services.util import safe_filename

bp = Blueprint("documents", __name__, url_prefix="/documents")

@bp.get("/")
def form():
    return render_template("documents.html", candidates=None)

@bp.post("/list")
def load():
    name = (flask_request.form.get("name") or "").strip()
    period = (flask_request.form.get("period") or "").strip() or None
    selected_id = (flask_request.form.get("company_id") or "").strip() or None
    try:
        candidates = search_companies(name, limit=100)
        if not candidates:
            return render_template("documents.html", name=name, candidates=None, message="Keine Treffer gefunden.")
        if not selected_id:
            return render_template("documents.html", name=name, period=period, candidates=candidates[:50],
                                   info="Bitte Firma auswählen und erneut senden.")
        docs = list_documents(selected_id, period)
        return render_template("documents.html", name=name, period=period, candidates=candidates[:50],
                               selected_id=selected_id, docs=docs, message=f"{len(docs)} Dokument(e) geladen.")
    except DatalandError as e:
        return render_template("documents.html", name=name, candidates=None, error=str(e))

@bp.get("/proxy-download/<string:document_id>")
def proxy_download(document_id: str):
    if not document_id:
        abort(400, "documentId fehlt")
    requested_name = flask_request.args.get("filename") or ""
    filename = safe_filename(requested_name, f"{document_id}.pdf")
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"
    try:
        upstream = stream_document(document_id)
    except DatalandError as e:
        abort(502, str(e))
    ct = upstream.headers.get("Content-Type", "application/pdf").split(";")[0].strip().lower()
    cl = upstream.headers.get("Content-Length")
    def generate():
        try:
            for chunk in upstream.iter_content(chunk_size=1024 * 64):
                if chunk:
                    yield chunk
        finally:
            upstream.close()
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    if cl and cl.isdigit():
        headers["Content-Length"] = cl
    return Response(generate(), headers=headers, mimetype=ct)

@bp.get("/view/<string:document_id>")
def inline_view(document_id: str):
    if not document_id:
        abort(400, "documentId fehlt")
    requested_name = flask_request.args.get("filename") or ""
    filename = safe_filename(requested_name, f"{document_id}.pdf")
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"
    try:
        upstream = stream_document(document_id)
    except DatalandError as e:
        abort(502, str(e))
    ct = upstream.headers.get("Content-Type", "application/pdf").split(";")[0].strip().lower()
    cl = upstream.headers.get("Content-Length")
    def generate():
        try:
            for chunk in upstream.iter_content(chunk_size=1024 * 64):
                if chunk:
                    yield chunk
        finally:
            upstream.close()
    headers = {"Content-Disposition": f'inline; filename="{filename}"'}
    if cl and cl.isdigit():
        headers["Content-Length"] = cl
    return Response(generate(), headers=headers, mimetype=ct)
