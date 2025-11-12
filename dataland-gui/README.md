# Dataland GUI

Einheitliche Web‑GUI (Flask) für:
- Firmensuche (/api/companies/names)
- SFDR‑Abruf (/api/data/sfdr/companies/{companyId})
- Dokumentliste & Download (/documents, /documents/{id})

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
echo "DEIN_API_KEY" > apikey.txt  # oder .env
python -m dataland_gui
```
