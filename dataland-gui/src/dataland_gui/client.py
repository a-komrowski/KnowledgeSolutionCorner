from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os
import requests
from .config import SETTINGS

class DatalandError(Exception):
    pass

@dataclass
class Company:
    company_id: str
    company_name: str

@dataclass
class Document:
    document_id: str
    document_name: str
    document_category: Optional[str]
    reporting_period: Optional[str]

def _read_api_key() -> Optional[str]:
    if SETTINGS.api_key_env:
        return SETTINGS.api_key_env.strip() or None
    try:
        if os.path.exists(SETTINGS.api_key_file):
            with open(SETTINGS.api_key_file, "r", encoding="utf-8") as f:
                k = f.read().strip()
                return k or None
    except Exception:
        pass
    return None

def _auth_headers() -> dict:
    headers = {"Accept": "application/json"}
    key = _read_api_key()
    if key:
        headers["Authorization"] = f"Bearer {key}"
    return headers

def search_companies(name: str, *, limit: int = 100, timeout: float | None = None) -> List[Company]:
    if not name:
        return []
    url = f"{SETTINGS.base_url}/api/companies/names"
    params = {"searchString": name, "resultLimit": limit}
    try:
        resp = requests.get(url, params=params, headers=_auth_headers(), timeout=timeout or SETTINGS.http_timeout)
        resp.raise_for_status()
        data = resp.json()
        return [
            Company(company_id=i.get("companyId", ""), company_name=i.get("companyName", ""))
            for i in data if isinstance(i, dict)
        ]
    except requests.RequestException as exc:
        raise DatalandError(f"HTTP/Netzwerkfehler bei search_companies: {exc}") from exc
    except Exception as exc:
        raise DatalandError(f"Unerwartetes Antwortformat bei search_companies: {exc}") from exc

def get_company_sfdr(company_id: str, *, reporting_period: Optional[int | str] = None,
                     show_only_active: bool = True, timeout: float | None = None) -> Dict[str, Any] | List[Any]:
    url = f"{SETTINGS.base_url}/api/data/sfdr/companies/{company_id}"
    params: Dict[str, Any] = {"showOnlyActive": str(show_only_active).lower()}
    if reporting_period is not None:
        params["reportingPeriod"] = str(reporting_period)
    try:
        resp = requests.get(url, params=params, headers=_auth_headers(), timeout=timeout or SETTINGS.http_timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as exc:
        raise DatalandError(f"HTTP/Netzwerkfehler bei get_company_sfdr: {exc}") from exc
    except ValueError as exc:
        raise DatalandError(f"Antwort ist kein gültiges JSON: {exc}") from exc

def list_documents(company_id: str, reporting_period: Optional[str] = None) -> List[Document]:
    if not company_id:
        return []
    url = f"{SETTINGS.base_url}/documents"
    params: Dict[str, Any] = {"companyId": company_id}
    if reporting_period:
        params["reportingPeriod"] = str(reporting_period)
    try:
        resp = requests.get(url, params=params, headers=_auth_headers(), timeout=SETTINGS.http_timeout)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            return []
        return [
            Document(
                document_id=o.get("documentId", ""),
                document_name=o.get("documentName", ""),
                document_category=o.get("documentCategory"),
                reporting_period=str(o.get("reportingPeriod")) if o.get("reportingPeriod") is not None else None,
            )
            for o in data if isinstance(o, dict)
        ]
    except requests.RequestException as exc:
        raise DatalandError(f"HTTP/Netzwerkfehler bei list_documents: {exc}") from exc

def stream_document(document_id: str) -> requests.Response:
    url = f"{SETTINGS.base_url}/documents/{document_id}"
    headers = _auth_headers()
    headers.setdefault("Accept", "*/*")
    try:
        resp = requests.get(url, headers=headers, timeout=SETTINGS.http_timeout, stream=True)
        resp.raise_for_status()
        return resp
    except requests.RequestException as exc:
        raise DatalandError(f"HTTP/Netzwerkfehler beim Dokumentabruf: {exc}") from exc
