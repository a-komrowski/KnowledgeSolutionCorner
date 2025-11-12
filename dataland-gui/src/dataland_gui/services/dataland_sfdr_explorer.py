from __future__ import annotations
from typing import Dict, List, Optional, Tuple
import json, time, requests
from ..config import SETTINGS

BASE = f"{SETTINGS.base_url}/api"
RETRY = 2
TIMEOUT = 20
SLEEP = 0.15

_session_singleton: Optional[requests.Session] = None

def _read_api_key() -> Optional[str]:
    import os
    key = os.getenv("DATALAND_API_KEY")
    if key:
        return key.strip() or None
    path = f"{os.getcwd()}/apikey.txt"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                k = f.read().strip()
                return k or None
        except Exception:
            return None
    return None

def _session() -> requests.Session:
    global _session_singleton
    if _session_singleton:
        return _session_singleton
    s = requests.Session()
    s.headers.update({"Accept": "application/json", "User-Agent": "dataland-gui/0.1"})
    key = _read_api_key()
    if key:
        s.headers["Authorization"] = f"Bearer {key}"
    _session_singleton = s
    return s

def _get_json(url: str):
    s = _session()
    for i in range(RETRY + 1):
        try:
            r = s.get(url, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (204, 404):
                return None
            time.sleep(0.3 * (i + 1))
        except requests.RequestException:
            time.sleep(0.5 * (i + 1))
    return None

def fetch_company_metadata(company_id: str, reporting_period: Optional[str], show_only_active: bool, qa_status: Optional[str]) -> List[dict]:
    params = []
    if company_id:
        params.append(f"companyId={company_id}")
    if show_only_active:
        params.append("showOnlyActive=true")
    if reporting_period:
        params.append(f"reportingPeriod={reporting_period}")
    if qa_status:
        params.append(f"qaStatus={qa_status}")
    url = f"{BASE}/metadata?{'&'.join(params)}"
    data = _get_json(url) or []
    return data if isinstance(data, list) else []

def fetch_data_points_map(data_id: str) -> Dict[str, str]:
    url = f"{BASE}/metadata/{data_id}/data-points"
    data = _get_json(url)
    return data if isinstance(data, dict) else {}

def try_fetch_value_for_datapoint(dp_id: str) -> Tuple[bool, Optional[dict]]:
    paths = [
        f"{BASE}/data-points/{dp_id}",
        f"{BASE}/data-points/{dp_id}/value",
        f"{BASE}/data-points/{dp_id}/values",
        f"{BASE}/data-points/{dp_id}/data",
    ]
    for url in paths:
        payload = _get_json(url)
        if not payload:
            continue
        if isinstance(payload, dict):
            for k in ("value", "values", "data", "amount", "numericValue"):
                if k in payload and payload[k] not in (None, "", [], {}):
                    return True, payload
            if any(isinstance(v, (int, float, str)) for v in payload.values()):
                return True, payload
        if isinstance(payload, list) and payload:
            return True, {"values": payload}
    return False, None

def fetch_datapoint_metadata(dp_id: str) -> Optional[dict]:
    url = f"{BASE}/data-points/{dp_id}/metadata"
    data = _get_json(url)
    return data if isinstance(data, dict) else None

def collect_datapoints_with_values(company_id: str, reporting_period: Optional[str], show_only_active: bool, qa_status: Optional[str]) -> List[dict]:
    meta = fetch_company_metadata(company_id, reporting_period, show_only_active, qa_status)
    data_ids = [m["dataId"] for m in meta if isinstance(m, dict) and m.get("currentlyActive")]
    rows: List[dict] = []
    for did in data_ids:
        time.sleep(SLEEP)
        dp_map = fetch_data_points_map(did)
        for dp_type, dp_id in dp_map.items():
            time.sleep(SLEEP)
            has_val, payload = try_fetch_value_for_datapoint(dp_id)
            if not has_val:
                continue
            md = fetch_datapoint_metadata(dp_id) or {}
            rows.append({
                "dataId": did,
                "dataPointType": dp_type,
                "dataPointId": dp_id,
                "hasValue": True,
                "valueSnippet": json.dumps(payload, ensure_ascii=False)[:400],
                "reportingPeriod": md.get("reportingPeriod"),
                "qaStatus": md.get("qaStatus"),
                "currentlyActive": md.get("currentlyActive"),
            })
    return rows
