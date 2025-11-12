from pathlib import Path
from typing import Optional, Dict, Any, List
from ..persist import create_envelope, append_jsonl
from ..config import settings
from ..http import DatalandHTTPSession

# Kandidaten für API-basierte Firmensuche:
# - Jedes Dict enthält den aufzurufenden Pfad und den Query-Parameter, in den der Suchstring eingesetzt wird.
API_CANDIDATES = [
    {"path": "/companies/names", "param_key": "searchString"},
]

#TODO überarbeiten
DOC_CANDIDATES = [
    {"path": "/", "param_key": "q"},
    {"path": "/search", "param_key": "q"},
    {"path": "/", "param_key": "query"},
    {"path": "/search", "param_key": "query"},
    {"path": "/companies/search", "param_key": "q"},
    {"path": "/documents/search", "param_key": "q"},
]

def _extract_company_list(data: Any) -> Optional[List[Dict[str, Any]]]:
    """
    Versucht, eine Firmenliste aus verschiedenen gängigen Response-Strukturen zu extrahieren.

    Unterstützte Formen:
        - Dict mit einem der Schlüssel: "companies", "results", "data", "items", "entities", "documents"
          (Wert jeweils eine Liste von Objekten)
        - Die Response selbst ist bereits eine Liste

    Args:
        data: Beliebige API-Antwort (bereits JSON-dekodiert).

    Returns:
        Liste mit Firmenobjekten oder None, wenn keine passende Struktur gefunden wurde.
    """
    if isinstance(data, dict):
        for k in ("companies","results","data","items","entities","documents"):
            v = data.get(k)
            if isinstance(v, list):
                return v
    if isinstance(data, list):
        return data
    return None

def search_company_via_api(api: DatalandHTTPSession, query:str, raw_dir:Path) -> Optional[Dict[str, Any]]:
    """
    Sucht ein Unternehmen über API-Endpunkte und liefert die erste gefundene Übereinstimmung.

    Ablauf:
        - Probiert nacheinander alle Einträge in API_CANDIDATES.
        - Persistiert jede Antwort (inkl. Status/Fehler) als JSONL-Envelope unter raw_dir.
        - Extrahiert die erste Firma aus der Antwortliste und normalisiert einige Kernfelder.

    Args:
        api: Initialisierte HTTP-Session für die API.
        query: Suchbegriff (Firmenname o. ä.).
        raw_dir: Verzeichnis, in das die Rohantworten geschrieben werden.

    Returns:
        Dict mit normalisierten Feldern:
            {
                "company_id": str | None,
                "name": str | None,
                "sector": str | None,
                "country": str | None,
                "source": "api",
                "raw": Dict[str, Any]  # ursprüngliches Item
            }
        oder None, falls keine Treffer gefunden wurden.
    """
    for c in API_CANDIDATES:
        endpoint, params = c["path"], {c["param_key"]: query}
        res = api.get(endpoint, params=params, timeout=settings.timeout_search)
        append_jsonl(raw_dir / "company_lookup_api.jsonl",
                     create_envelope(endpoint, res["status"], params, res.get("data"), res.get("error")))
        if res["status"]==200 and res["data"]:
            companies = _extract_company_list(res["data"])
            if not companies: 
                continue
            item = companies[0]
            return dict(
                company_id = item.get("companyId") or item.get("id") or item.get("dataId"),
                name       = item.get("companyName") or item.get("name") or item.get("company"),
                sector     = item.get("sector"),
                country    = item.get("countryCode") or item.get("country"),
                source     = "api",
                raw        = item,
            )
    return None

def search_company_via_documents(doc: DatalandHTTPSession, query:str, raw_dir:Path)->Optional[Dict[str,Any]]:
    """
    Sucht ein Unternehmen über dokumentenorientierte Endpunkte und liefert die erste Übereinstimmung.

    Ablauf:
        - Probiert nacheinander alle Einträge in DOC_CANDIDATES.
        - Persistiert jede Antwort (inkl. Status/Fehler) als JSONL-Envelope unter raw_dir.
        - Extrahiert die erste Firma aus der Antwortliste und normalisiert einige Kernfelder.

    Args:
        doc: HTTP-Session für den Dokumenten-Endpunkt.
        query: Suchbegriff.
        raw_dir: Verzeichnis, in das die Rohantworten geschrieben werden.

    Returns:
        Dict mit normalisierten Feldern:
            {
                "company_id": str | None,
                "name": str | None,
                "sector": str | None,
                "country": str | None,
                "source": "documents",
                "raw": Dict[str, Any]
            }
        oder None, falls keine Treffer gefunden wurden.
    """
    for c in DOC_CANDIDATES:
        endpoint, params = c["path"], {c["param_key"]: query}
        res = doc.get(endpoint, params=params, timeout=settings.timeout_search)
        append_jsonl(raw_dir / "company_lookup_documents.jsonl",
                     create_envelope(endpoint, res["status"], params, res.get("data"), res.get("error")))
        if res["status"]==200 and res["data"]:
            companies = _extract_company_list(res["data"])
            if not companies:
                continue
            item = companies[0]
            return dict(
                company_id = item.get("companyId") or item.get("id") or item.get("dataId"),
                name       = item.get("companyName") or item.get("name"),
                sector     = item.get("sector"),
                country    = item.get("countryCode") or item.get("country"),
                source     = "documents",
                raw        = item,
            )
    return None
