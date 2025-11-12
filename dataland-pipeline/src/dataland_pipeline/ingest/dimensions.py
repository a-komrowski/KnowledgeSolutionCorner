from __future__ import annotations

from typing import Any, Dict, List, Optional
import logging
from pathlib import Path

from ..config import settings
from ..http import DatalandHTTPSession
from ..persist import append_jsonl, create_envelope

log = logging.getLogger(__name__)


def _extract_dimensions(payload: Any) -> Optional[List[Dict[str, Any]]]:
    """
    Versucht, die Dimensions-Liste aus unterschiedlichen Schemas herauszuziehen.
    """
    if isinstance(payload, dict):
        for key in ("availableDataPoints", "dimensions", "dataPoints", "data", "results", "items"):
            val = payload.get(key)
            if isinstance(val, list):
                return val
    if isinstance(payload, list):
        return payload
    return None


def list_available_dimensions(
    api_session: DatalandHTTPSession,
    company_id: str,
    raw_dir: Path,
    reporting_years: int = 5,
) -> Optional[List[Dict[str, Any]]]:
    """
    Fragt verfügbare Datendimensionen für ein Unternehmen ab und persistiert die Rohantwort.

    Args:
        api_session: Dataland HTTPSession (API-Service)
        company_id: Unternehmens-ID
        raw_dir: Verzeichnis für Raw-Daten (jsonl)
        reporting_years: Wie viele Jahre rückwirkend abgefragt werden

    Returns:
        Liste von Dimensionen (dict) oder None bei Fehler/Leer.
    """
    from datetime import datetime

    endpoint = "/metadata/available-data-dimensions"
    year_now = datetime.now().year
    params: Dict[str, Any] = {
        "companyIds": [company_id],               # Plural + Array
        "reportingPeriodFrom": year_now - reporting_years,
        "reportingPeriodTo": year_now,
    }

    log.info("Fetch available dimensions: company_id=%s years=%s..%s",
             company_id, params["reportingPeriodFrom"], params["reportingPeriodTo"])
    res = api_session.get(endpoint, params=params, timeout=settings.timeout_data)

    # persist raw
    append_jsonl(raw_dir / "available_dimensions.jsonl",
                 create_envelope(endpoint, res["status"], params, res.get("data"), error=res.get("error")))

    if res["status"] != 200:
        log.warning("Available dimensions failed: status=%s error=%s", res["status"], res.get("error"))
        return None

    dims = _extract_dimensions(res.get("data"))
    if not dims:
        log.warning("Available dimensions empty for company_id=%s", company_id)
        return None

    # Kleine Vorschau ins Log
    preview = []
    for d in dims[:10]:
        dp_id = d.get("dataPointId") or d.get("id") or "?"
        indicator = d.get("indicator") or d.get("metric") or d.get("code") or "?"
        period = d.get("period") or d.get("year") or "?"
        preview.append(f"{indicator}({period})[{dp_id}]")
    if preview:
        log.info("Found %d dimensions. Preview: %s%s",
                 len(dims), ", ".join(preview[:5]), " ..." if len(preview) > 5 else "")

    return dims
