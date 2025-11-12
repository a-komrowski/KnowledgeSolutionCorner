import json, hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def nowz() -> str:
    """
    Gibt aktuellen UTC-Zeitstempel im ISO-Format zurück.
    
    Returns:
        String wie "2025-11-05T13:45:12Z"
    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def append_jsonl(path: Path, obj: dict) -> None:
    """
    Fügt ein JSON-Objekt als neue Zeile zu einer JSONL-Datei hinzu.

    Args:
        path: Pfad zur JSONL-Datei
        obj: Dictionary, das gespeichert werden soll
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def create_envelope(endpoint: str, status: int, request_params: dict, payload: Any, error: Any|None=None) -> dict:
    """
    Envelope mit Metadaten + optionalem Fehlerfeld erstellen.
    - endpoint: aufgerufener API-Pfad (ohne Base-URL)
    - status: HTTP-Statuscode (oder -1 bei Ausnahme)
    - request_params: Query-Parameter
    - payload: Response-Body (roh)
    - error: optionaler Fehlertext/-objekt
    """
    env = {
        "ts": nowz(),
        "endpoint": endpoint,
        "status": status,
        "request": {"params": request_params},
        "payload": payload
    }
    if error is not None:
        env["error"] = error
    return env

def generate_hash(company_id: str, data_point_id: str|None=None, period: str|None=None) -> str:
    """
    Generiert einen SHA256-Hash für Idempotenz-Checks.
    
    Verhindert, dass dieselben Daten mehrfach gespeichert werden.
    
    Args:
        company_id: Die Unternehmens-ID
        data_point_id: Optional - Datenpunkt-ID
        period: Optional - Periode
        
    Returns:
        Hexadezimaler Hash-String
    """
    key = f"{company_id}:{data_point_id or ''}:{period or ''}"
    return hashlib.sha256(key.encode()).hexdigest()
