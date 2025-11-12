from __future__ import annotations

from typing import Any, Dict, List, Optional
import logging, time
from pathlib import Path

from ..config import settings
from ..http import DatalandHTTPSession
from ..persist import append_jsonl, create_envelope, generate_hash, nowz

log = logging.getLogger(__name__)

def _dim_to_request_params(company_id: str, dim: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formt ein Dimensions-Objekt in Request-Parameter für den Werte-Endpunkt um.

    Unterstützte Felder in `dim`:
        - ID:   "dataPointId" | "id"
        - Zeit: "period" | "year"

    Args:
        company_id: Eindeutige ID des Unternehmens für die Abfrage.
        dim:       Dimensions-Objekt eines Datenpunkts (z. B. aus einer vorangegangenen Suche).

    Returns:
        Dict mit minimal notwendigen Parametern für den Request, z. B.:
        {"companyId": "<id>", "dataPointId": "<dp_id>", "period": 2023}
        (Felder werden nur gesetzt, wenn vorhanden.)
    """
    data_point_id = dim.get("dataPointId") or dim.get("id")
    period = dim.get("period") or dim.get("year")
    params: Dict[str, Any] = {"companyId": company_id}
    if data_point_id:
        params["dataPointId"] = data_point_id
    if period is not None:
        params["period"] = period
    return params

def fetch_all_values(
    api_session: DatalandHTTPSession,
    company_id: str,
    dimensions: List[Dict[str, Any]],
    raw_dir: Path,
) -> Dict[str, Any]:
    """
    Ruft Werte für eine Menge von Datenpunkt-Dimensionen ab und protokolliert jede Antwort als JSONL.

    Verhalten:
        - Für jede Dimension wird ein GET auf "/data-points/values" abgesetzt.
        - Doppelte Anfragen (gleiche Kombination aus companyId, dataPointId, period) werden übersprungen.
        - Antworten werden als Envelopes in eine zeitgestempelte *.jsonl-Datei geschrieben.
        - Fortschritt/Rate werden periodisch geloggt.

    Args:
        api_session: Vorbereitete HTTP-Session zur Dataland-API.
        company_id:  Unternehmens-ID, für die Werte abgefragt werden.
        dimensions:  Liste von Dimensionen (mindestens "dataPointId"/"id"; optional "period"/"year",
                     "indicator"/"name" nur für Fehlermeldungen).
        raw_dir:     Verzeichnis, in das die Rohantworten (JSONL) persistiert werden.

    Returns:
        Statistikdict mit Feldern:
            {
                "total": int,                  # Anzahl übergebener Dimensionen
                "success": int,                # erfolgreiche Antworten (HTTP 200)
                "failed": int,                 # fehlgeschlagene Antworten (inkl. Netzwerk-/Serverfehler)
                "skipped_duplicates": int,     # übersprungene Duplikate
                "errors": List[str],           # Fehlermeldungen je fehlgeschlagenem Item
                "outfile": str                 # Pfad zur JSONL-Ausgabedatei
            }

    Hinweise:
        - Timeout je Request wird aus `settings.timeout_values` genommen.
        - Die Rückgaben der API werden ungeprüft als `data` in den Envelope geschrieben.
        - Die Methode selbst implementiert kein Retry; Retries/Backoff liegen in `DatalandHTTPSession`.
    """
    endpoint = "/data-points/values"
    timestamp = nowz().replace(":", "").replace("-", "").replace("Z", "")
    values_file = raw_dir / f"values_{timestamp}.jsonl"

    stats = {
        "total": len(dimensions),
        "success": 0,
        "failed": 0,
        "skipped_duplicates": 0,
        "errors": [],
        "outfile": str(values_file),
    }
    seen_hashes: set[str] = set()

    if not dimensions:
        log.warning("fetch_all_values called with empty dimensions list.")
        return stats

    log.info("Fetching values for %d data points (company_id=%s)", len(dimensions), company_id)
    start_time = time.time()

    # Alle ~10% ein Fortschrittslog; bei kleinen Listen min. jede 1.
    progress_step = max(1, len(dimensions) // 10)

    for i, dim in enumerate(dimensions, start=1):
        data_point_id = dim.get("dataPointId") or dim.get("id")
        period = dim.get("period") or dim.get("year")
        indicator = dim.get("indicator") or dim.get("name") or "Unknown"

        if not data_point_id:
            stats["failed"] += 1
            msg = f"Missing dataPointId for indicator={indicator} (idx={i})"
            stats["errors"].append(msg)
            append_jsonl(values_file, create_envelope(endpoint, 0, {"companyId": company_id}, None, error=msg))
            continue

        hash_key = generate_hash(company_id, data_point_id, str(period) if period is not None else None)
        if hash_key in seen_hashes:
            stats["skipped_duplicates"] += 1
            continue
        seen_hashes.add(hash_key)

        params = _dim_to_request_params(company_id, dim)
        res = api_session.get(endpoint, params=params, timeout=settings.timeout_values)
        append_jsonl(values_file, create_envelope(endpoint, res["status"], params, res.get("data"), error=res.get("error")))

        if res["status"] == 200:
            stats["success"] += 1
        else:
            stats["failed"] += 1
            stats["errors"].append(f"{indicator}({period}): {res.get('error')}")

        if i % progress_step == 0 or i == 1 or i == len(dimensions):
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0.0
            log.info("Progress %d/%d (%.1f%%) | ok=%d fail=%d dup=%d | %.1f req/s",
                     i, len(dimensions), (i / len(dimensions)) * 100,
                     stats["success"], stats["failed"], stats["skipped_duplicates"], rate)

    elapsed_total = time.time() - start_time
    if elapsed_total > 0:
        log.info("Values done: total=%d ok=%d fail=%d dup=%d | duration=%.1fs | rate=%.1f req/s | out=%s",
                 stats["total"], stats["success"], stats["failed"], stats["skipped_duplicates"],
                 elapsed_total, stats["total"] / elapsed_total, values_file.name)
    else:
        log.info("Values done: total=%d out=%s", stats["total"], values_file.name)

    return stats
