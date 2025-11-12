from __future__ import annotations
import time, logging, requests
from typing import Any

log = logging.getLogger(__name__)

class DatalandHTTPSession:
    """
    HTTP-Session mit Retry-Logik, exponentiellem Backoff und optionaler Token-Authentifizierung.

    Diese Klasse kapselt die gesamte HTTP-Kommunikation mit der Dataland-API:
    - Wiederholungsversuche bei 429 (Rate Limit) sowie 5xx-Antworten
    - exponentielles Backoff zwischen den Versuchen, begrenzt durch `backoff_max`
    - konsistente Rückgabestruktur für erfolgreiche und fehlerhafte Antworten
    - einfache Statistikzählung über alle Requests
    """

    def __init__(self, base_url: str, api_token: str|None, *, max_retries:int, backoff_base:int, backoff_max:int):
        """
        Initialisiert die Session und setzt Header, Retry- und Backoff-Parameter.

        Args:
            base_url: Basis-URL des API-Endpunkts (z. B. "https://example.com/api"); nachgestellter Slash wird entfernt.
            api_token: Optionales Bearer-Token für die Authentifizierung. Ist `None`, wird ohne Authentifizierung gearbeitet
                (Log-Hinweis „mock mode“).
            max_retries: Maximale Anzahl an Wiederholungsversuchen für einen Request (inkl. des letzten Versuchs ohne erneutes Warten).
            backoff_base: Basiswert (Sekunden) für das exponentielle Backoff pro Versuch.
            backoff_max: Obergrenze (Sekunden) für die Backoff-Wartezeit je Versuch.

        Hinweise:
            - Es wird eine `requests.Session` mit JSON-Standardheadern erzeugt.
            - Bei vorhandenem Token wird es als `Authorization`-Header gesetzt (Form: unverändert weitergereicht).
        """
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.backoff_max = backoff_max

        self.session = requests.Session()
        headers = {"Content-Type": "application/json","Accept": "application/json"}
        if api_token:
            headers["Authorization"] = api_token
            log.info("Session for %s with token present", self.base_url)
        else:
            log.warning("Session for %s without token (mock mode)", self.base_url)
        self.session.headers.update(headers)

        self._stats = dict(total_requests=0, successful_requests=0, failed_requests=0, retries=0, rate_limits=0)

    def _backoff(self, attempt: int) -> float:
        """
        Berechnet die Wartezeit für den gegebenen Versuch gemäß exponentiellem Backoff.

        Args:
            attempt: 1-basierter Zähler des aktuellen Versuchs.

        Returns:
            float: Wartezeit in Sekunden (`min(backoff_base ** attempt, backoff_max)`).
        """
        return min(self.backoff_base ** attempt, self.backoff_max)

    def get(self, endpoint: str, params: dict|None=None, timeout:int=30) -> dict[str, Any]:
        """
        Führt einen GET-Request mit Retry-/Backoff-Logik aus.

        Verhalten:
            - 200: Erfolg, JSON-Body wird unter `data` zurückgegeben.
            - 429: Zählt als Rate-Limit, es wird nach Backoff gewartet und erneut versucht (bis `max_retries`).
            - 5xx: Serverfehler → Retries mit Backoff bis zur Maximalanzahl; anschließend Fehler.
            - Sonstige Statuscodes: Kein Retry; Rückgabe mit Fehlermeldung und ggf. Antwort-Body (JSON oder Text).
            - Netzwerk-/`requests`-Ausnahmen: Retries bis `max_retries`, danach Fehler.

        Args:
            endpoint: Pfad relativ zu `base_url` (z. B. "/documents").
            params: Optionale Query-Parameter.
            timeout: Timeout pro Versuch in Sekunden.

        Returns:
            dict[str, Any]: Einheitliches Ergebnisobjekt:
                {
                    "status": int,         # HTTP-Statuscode (oder 0 bei Netzwerkfehler/überschrittenen Retries)
                    "data": Any | None,    # Antwortdaten bei Erfolg (i. d. R. dict), sonst None
                    "error": str | None    # Fehlermeldung bei Nicht-Erfolg, sonst None
                }

        Nebenwirkungen:
            - Aktualisiert die in `get_stats()` auslesbaren Zähler (`total_requests`, `successful_requests`,
              `failed_requests`, `retries`, `rate_limits`).
            - Wartet zwischen Versuchen jeweils gemäß `_backoff()`.
        """
        url = f"{self.base_url}{endpoint}"
        params = params or {}
        self._stats["total_requests"] += 1
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = self.session.get(url, params=params, timeout=timeout)
                if resp.status_code == 200:
                    self._stats["successful_requests"] += 1
                    return {"status":200, "data":resp.json(), "error":None}
                if resp.status_code == 429:
                    self._stats["rate_limits"] += 1
                    wait = self._backoff(attempt)
                    import time as _t; _t.sleep(wait)
                    self._stats["retries"] += 1
                    continue
                if 500 <= resp.status_code < 600:
                    if attempt < self.max_retries:
                        wait = self._backoff(attempt)
                        import time as _t; _t.sleep(wait)
                        self._stats["retries"] += 1
                        continue
                    self._stats["failed_requests"] += 1
                    return {"status":resp.status_code, "data":None, "error":f"Server error after retries"}
                self._stats["failed_requests"] += 1
                try: err = resp.json()
                except Exception: err = resp.text
                return {"status":resp.status_code, "data":None, "error":f"HTTP {resp.status_code}: {err}"}
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries:
                    wait = self._backoff(attempt)
                    import time as _t; _t.sleep(wait)
                    self._stats["retries"] += 1
                else:
                    self._stats["failed_requests"] += 1
                    return {"status":0,"data":None,"error":f"Network error: {e}"}
        # Sollte nie erreicht werden
        self._stats["failed_requests"] += 1
        return {"status":0,"data":None,"error":"Max retries exceeded"}

    def get_stats(self) -> dict:
        """
        Liefert eine Momentaufnahme der Request-Statistiken seit Instanziierung.

        Returns:
            dict: {
                "total_requests": int,     # Anzahl aller gestarteten Requests
                "successful_requests": int,# Anzahl erfolgreicher (Status 200)
                "failed_requests": int,    # Anzahl gescheiterter (inkl. nach Retries)
                "total_retries": int,      # Summe aller Wiederholungsversuche
                "rate_limits_hit": int     # Anzahl 429-Antworten
            }
        """
        return dict(
            total_requests=self._stats["total_requests"],
            successful_requests=self._stats["successful_requests"],
            failed_requests=self._stats["failed_requests"],
            total_retries=self._stats["retries"],
            rate_limits_hit=self._stats["rate_limits"],
        )
