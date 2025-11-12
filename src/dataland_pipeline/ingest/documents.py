from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
import logging
from pathlib import Path

from ..config import settings
from ..http import DatalandHTTPSession
from ..persist import append_jsonl, create_envelope

log = logging.getLogger(__name__)

# Probing-Kandidaten für den Documents-Service:
# Jedes Tupel ist (Endpoint, Query-Parametername).
_DOC_CANDIDATES: Tuple[Tuple[str, str], ...] = (
    ("/", "q"),
    ("/search", "q"),
    ("/", "query"),
    ("/search", "query"),
)


def _extract_documents(payload: Any) -> Optional[List[Dict[str, Any]]]:
    """
    Extrahiert eine Dokumentliste aus verschiedenen gängigen Response-Formaten.

    Unterstützte Formen:
        - Dict mit einem der Schlüssel: "documents", "results", "data", "items" (Wert jeweils Liste)
        - Die Response selbst ist bereits eine Liste

    Args:
        payload: JSON-dekodierte Antwort des Services.

    Returns:
        Liste von Dokumentobjekten oder None, wenn keine passende Struktur gefunden wurde.
    """
    if isinstance(payload, dict):
        for key in ("documents", "results", "data", "items"):
            val = payload.get(key)
            if isinstance(val, list):
                return val
    if isinstance(payload, list):
        return payload
    return None


def search_documents(
    doc_session: DatalandHTTPSession,
    query: str,
    company_id: Optional[str],
    raw_dir: Path,
) -> Optional[List[Dict[str, Any]]]:
    """
    Sucht Dokumente im Documents-Service und persistiert alle Probing-Antworten als JSONL.

    Verhalten:
        - Probiert mehrere Endpunkt-/Parameter-Kombinationen (siehe `_DOC_CANDIDATES`) nacheinander aus.
        - Testet jeweils sowohl ohne als auch – falls vorhanden – mit `companyId`.
        - Persistiert jede Antwort als Envelope in `document_search.jsonl`.
        - Bricht beim ersten erfolgreichen Treffer (HTTP 200 + Daten vorhanden) ab und gibt die extrahierte
          Dokumentliste zurück. Liefert None, wenn kein Kandidat erfolgreich ist oder die Payload leer ist.

    Args:
        doc_session: Initialisierte HTTP-Session für den Documents-Service.
        query:       Suchbegriff (frei).
        company_id:  Optionale Unternehmens-ID zur Eingrenzung der Suche.
        raw_dir:     Verzeichnis, in das Rohantworten (JSONL) geschrieben werden.

    Returns:
        Liste von Dokumentobjekten (Dicts) oder None, wenn keine Dokumente gefunden wurden.
    """
    log.info("Searching documents for query=%r company_id=%r", query, company_id)

    # Kandidatenliste aufbauen: erst ohne, dann (falls vorhanden) mit companyId.
    candidates: List[Tuple[str, Dict[str, Any]]] = []
    for ep, key in _DOC_CANDIDATES:
        candidates.append((ep, {key: query}))
    if company_id:
        for ep, key in _DOC_CANDIDATES:
            candidates.append((ep, {key: query, "companyId": company_id}))

    successful = None
    for endpoint, params in candidates:
        res = doc_session.get(endpoint, params=params, timeout=settings.timeout_search)
        append_jsonl(raw_dir / "document_search.jsonl",
                     create_envelope(endpoint, res["status"], params, res.get("data"), error=res.get("error")))
        if res["status"] == 200 and res.get("data"):
            successful = res
            log.info("Documents probe success at %s with params keys=%s", endpoint, list(params.keys()))
            break
        else:
            log.debug("Documents probe failed at %s (status=%s)", endpoint, res["status"])

    if not successful:
        log.warning("No documents found for query=%r company_id=%r", query, company_id)
        return None

    documents = _extract_documents(successful.get("data"))
    if not documents:
        log.warning("Documents payload parsed empty for query=%r", query)
        return None

    # Kleine Statistik über Typen und Jahre (nur Logging, keine Validierung).
    types: Dict[str, int] = {}
    years: set[int] = set()
    for d in documents:
        t = d.get("documentType") or d.get("type") or "Unknown"
        types[t] = types.get(t, 0) + 1
        y = d.get("year") or d.get("reportingPeriod")
        if isinstance(y, int):
            years.add(y)

    log.info("Found %d documents. Types=%s Years=%s",
             len(documents), types, sorted(years) if years else "N/A")

    return documents
