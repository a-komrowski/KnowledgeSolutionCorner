# Dataland Pipeline

CLI-basierte Ingest-Pipeline (Dataland → Dimensions → Values → Documents), 
mit JSONL-Persistenz, Mocks und Notebook-Demo.

## Schnellstart

```bash
pip install -e .
cp .env.example .env   # Token eintragen (oder leer lassen für Mock-Modus)
dataland run --company "Siemens" --log-level INFO
```

Daten landen unter `data/raw/`. Für Experimente gibt es `notebooks/01_mvp_pipeline.ipynb`.
