from __future__ import annotations
from typing import Any, Dict, List, Optional
from .persist import append_jsonl, create_envelope, nowz

def create_run_log(api_session, doc_session, raw_dir, company_info, dimensions, values_stats, documents) -> Dict[str, Any]:
    """
    Erstellt und persistiert eine zusammenfassende Laufstatistik („Run Log“) für einen kompletten Dataland-Job.

    Das Run Log fasst die wichtigsten Ergebnisse und Metriken eines Durchlaufs zusammen:
        - Metadaten (Zeitstempel, Unternehmen, Treffer)
        - Zählwerte zu Dimensionen, Werten und Dokumenten
        - Aggregierte Statistiken beider HTTP-Sessions (API und Documents-Service)
        - Gesamtstatistik (Summen aller Requests, Erfolge, Fehler usw.)

    Args:
        api_session: Instanz von `DatalandHTTPSession` für den API-Service (liefert `get_stats()`).
        doc_session: Instanz von `DatalandHTTPSession` für den Documents-Service.
        raw_dir:     Zielverzeichnis, in dem die JSONL-Datei „run_log.jsonl“ abgelegt wird.
        company_info: Dict mit Basisinformationen über das gefundene Unternehmen (oder None).
        dimensions:   Liste aller abgefragten Dimensionen (kann leer sein).
        values_stats: Statistikdict aus `fetch_all_values()` (oder None).
        documents:    Liste gefundener Dokumente (kann leer oder None sein).

    Returns:
        Dict[str, Any]: Vollständiges Run-Log-Objekt mit Struktur:
            {
                "timestamp": str,
                "company_found": bool,
                "company_id": str | None,
                "dimensions_count": int,
                "values_success": int,
                "documents_count": int,
                "api_service": dict,
                "documents_service": dict,
                "total_statistics": dict
            }

    Nebenwirkungen:
        - Schreibt das Run Log als JSONL-Eintrag nach `<raw_dir>/run_log.jsonl`.
    """
    api_stats = api_session.get_stats()
    doc_stats = doc_session.get_stats()

    run_log = {
        "timestamp": nowz(),
        "company_found": bool(company_info),
        "company_id": company_info.get("company_id") if company_info else None,
        "dimensions_count": len(dimensions) if dimensions else 0,
        "values_success": values_stats.get("success") if values_stats else 0,
        "documents_count": len(documents) if documents else 0,
        "api_service": api_stats,
        "documents_service": doc_stats,
        "total_statistics": {
            "total_requests": api_stats["total_requests"] + doc_stats["total_requests"],
            "successful_requests": api_stats["successful_requests"] + doc_stats["successful_requests"],
            "failed_requests": api_stats["failed_requests"] + doc_stats["failed_requests"],
            "total_retries": api_stats["total_retries"] + doc_stats["total_retries"],
            "rate_limits_hit": api_stats["rate_limits_hit"] + doc_stats["rate_limits_hit"],
        }
    }
    append_jsonl(raw_dir / "run_log.jsonl", create_envelope("run_log", 200, {}, run_log))
    return run_log
