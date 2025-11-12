"""
Lokaler Einstiegspunkt für die Dataland-Pipeline.

Ermöglicht den CLI-Aufruf auch dann,
wenn das Projekt noch nicht mit `pip install -e .` installiert wurde.

Beispiel:
    python dataland.py run --company "Siemens" --log-level INFO
"""

from dataland_pipeline.cli import app

if __name__ == "__main__":
    app()
