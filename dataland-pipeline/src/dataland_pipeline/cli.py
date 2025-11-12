import typer
from .config import settings
from .logging import setup_logging
from .http import DatalandHTTPSession
from .ingest.lookup import search_company_via_api, search_company_via_documents
from .ingest.dimensions import list_available_dimensions
from .ingest.values import fetch_all_values
from .ingest.documents import search_documents
from .mocks.fixtures import create_mock_data_if_needed
from .runlog import create_run_log

app = typer.Typer(help="Dataland Ingest Pipeline", add_completion=False)


def _pipeline(company: str, log_level: str):
    setup_logging(log_level)

    api = DatalandHTTPSession(
        settings.base_url_api, settings.api_token,
        max_retries=settings.max_retries, backoff_base=settings.backoff_base, backoff_max=settings.backoff_max
    )
    doc = DatalandHTTPSession(
        settings.base_url_documents, settings.api_token,
        max_retries=settings.max_retries, backoff_base=settings.backoff_base, backoff_max=settings.backoff_max
    )

    raw = settings.raw_dir

    company_info = search_company_via_api(api, company, raw) or \
                   search_company_via_documents(doc, company, raw)

    dimensions = None
    values_stats = None
    documents = None

    if company_info and company_info.get("company_id"):
        cid = company_info["company_id"]
        dimensions = list_available_dimensions(api, cid, raw)
        if dimensions:
            values_stats = fetch_all_values(api, cid, dimensions, raw)
        documents = search_documents(doc, company, cid, raw)

    company_info, dimensions, values_stats, documents = create_mock_data_if_needed(
        company_info, dimensions, values_stats, documents, raw
    )

    create_run_log(api, doc, raw, company_info, dimensions, values_stats, documents)
    typer.secho(
        f"Run complete. Company: {company_info.get('name','N/A')} | "
        f"dims={len(dimensions) if dimensions else 0} | "
        f"values_ok={values_stats.get('success') if values_stats else 0} | "
        f"docs={len(documents) if documents else 0}",
        fg=typer.colors.GREEN
    )


# ---- Subcommand: run -------------------------------------------------
@app.command("run")
def run(
    company: str = typer.Option(settings.company_query, help="Suchbegriff/Company"),
    log_level: str = typer.Option("INFO", help="Loglevel (DEBUG, INFO, WARNING, ERROR)"),
):
    """Starte die Ingest-Pipeline."""
    _pipeline(company, log_level)


# ---- Optional: Default-Command (ohne 'run') --------------------------
@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    company: str = typer.Option(None, help="Suchbegriff/Company (wirkt nur, wenn kein Subcommand angegeben wird)"),
    log_level: str = typer.Option("INFO", help="Loglevel (DEBUG, INFO, WARNING, ERROR)"),
):
    """
    Wenn du 'dataland' ohne Unterbefehl aufrufst, wird automatisch die Pipeline ausgeführt.
    """
    if ctx.invoked_subcommand is None:
        _pipeline(company or settings.company_query, log_level)


if __name__ == "__main__":
    app()
