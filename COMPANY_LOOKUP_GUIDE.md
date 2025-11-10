# 🔍 Company-Lookup Implementation Guide

## Problem

Die Dataland-Swagger-Dokumentation zeigt **keinen eindeutigen Company-Search-Endpoint**:
- ✅ `/metadata/available-data-dimensions` ist dokumentiert
- ❌ `/metadata/companies/search` existiert nicht offiziell
- ❓ Unklar, wie man `company_id` vom Unternehmensnamen ableitet

## Lösung: Robuste Fallback-Strategie

### 3-Stufen-Architektur

```
┌─────────────────────────────────────────────────────────────┐
│ 1️⃣ API-Service Probing (Primärweg)                         │
│    → /metadata/companies/search?q=Siemens                   │
│    → /metadata/companies?query=Siemens                      │
│    → /companies/search?q=Siemens                            │
│    → /companies?name=Siemens                                │
│    → /entities/search?q=Siemens                             │
│    → /api/companies/search?q=Siemens                        │
└─────────────────────────────────────────────────────────────┘
                          ↓ (bei Fehler)
┌─────────────────────────────────────────────────────────────┐
│ 2️⃣ Documents-Service Probing (Fallback)                    │
│    → /?q=Siemens                                            │
│    → /search?q=Siemens                                      │
│    → /?query=Siemens                                        │
│    → /search?query=Siemens                                  │
│    → /companies/search?q=Siemens                            │
│    → /documents/search?q=Siemens                            │
└─────────────────────────────────────────────────────────────┘
                          ↓ (bei Fehler)
┌─────────────────────────────────────────────────────────────┐
│ 3️⃣ Mock-Modus (Last Resort)                                │
│    → Erstelle Test-Company mit fester ID                    │
│    → Erstelle Mock-Dimensions & Values                      │
│    → Ermöglicht Offline-Entwicklung                         │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Details

### CONFIG-Struktur

```python
CONFIG = {
    # Zwei separate Services
    "base_url_api": "https://dataland.com/api",
    "base_url_documents": "https://dataland.com/documents",
    
    # API-Service Kandidaten (Primärweg)
    "company_lookup_api_candidates": [
        {"path": "/metadata/companies/search", "params": {"q": None}},
        {"path": "/metadata/companies", "params": {"query": None}},
        {"path": "/companies/search", "params": {"q": None}},
        {"path": "/companies", "params": {"name": None}},
        {"path": "/entities/search", "params": {"q": None}},
        {"path": "/api/companies/search", "params": {"q": None}},
    ],
    
    # Documents-Service Kandidaten (Fallback)
    "company_lookup_doc_candidates": [
        {"path": "/", "params": {"q": None}},
        {"path": "/search", "params": {"q": None}},
        {"path": "/", "params": {"query": None}},
        {"path": "/search", "params": {"query": None}},
        {"path": "/companies/search", "params": {"q": None}},
        {"path": "/documents/search", "params": {"q": None}},
    ],
}
```

### Funktionen

#### 1. `search_company_via_api(api_session, query, raw_dir)`

- **Zweck:** Company-Lookup über API-Service
- **Sessions:** Nutzt `api_session` (base_url="/api")
- **Persistenz:** `raw/company_lookup_api.jsonl`
- **Return:** `company_info` dict oder `None`

#### 2. `search_company_via_documents(doc_session, query, raw_dir)`

- **Zweck:** Company-Lookup über Documents-Service (Fallback)
- **Sessions:** Nutzt `doc_session` (base_url="/documents")
- **Persistenz:** `raw/company_lookup_documents.jsonl`
- **Return:** `company_info` dict oder `None`

#### 3. `create_mock_data_if_needed()`

- **Zweck:** Mock-Daten für Offline-Entwicklung
- **Trigger:** Beide Lookup-Methoden fehlgeschlagen
- **Erstellt:** Company Info, Dimensions, Values, Documents

## Persistenz & Debugging

Alle Probe-Versuche werden in JSONL-Dateien gespeichert:

```bash
raw/
├── company_lookup_api.jsonl       # API-Service Probes
├── company_lookup_documents.jsonl # Documents-Service Probes
├── available_dimensions.jsonl     # Dimensions-Metadaten
├── values_*.jsonl                 # Datenpunkte
├── document_search.jsonl          # Dokumente
└── run_log.jsonl                  # Session-Statistiken
```

### Erfolgreichen Endpoint finden

```python
# Quick-Check nach dem ersten Run
import json

with open("raw/company_lookup_api.jsonl", 'r') as f:
    for line in f:
        entry = json.loads(line)
        if entry["status"] == 200:
            print(f"✅ Erfolg: {entry['endpoint']}")
            print(f"   Response: {entry['payload']}")
```

## Vorteile dieser Architektur

| Feature | Beschreibung |
|---------|--------------|
| **Resilience** | Funktioniert auch bei API-Änderungen |
| **Transparency** | Alle Versuche in JSONL → vollständige Audit-Trail |
| **Flexibility** | Neue Endpoints via CONFIG hinzufügen |
| **Debugging** | Klare Logs zeigen Erfolg/Fehler pro Endpoint |
| **Offline-Ready** | Mock-Modus für Entwicklung ohne API |
| **Production-Ready** | Kann auf einzelnen Endpoint reduziert werden |

## Produktiv-Optimierung

Sobald erfolgreicher Endpoint identifiziert:

```python
# Reduziere auf EINEN funktionierenden Endpoint
CONFIG["company_lookup_api_candidates"] = [
    {"path": "/metadata/companies/search", "params": {"q": None}}
]

# Oder falls nur Documents funktioniert, deaktiviere API-Probing:
CONFIG["company_lookup_api_candidates"] = []
```

Das spart API-Calls und beschleunigt den Lookup!

## Testing

```bash
# 1. Setup
cp .env.example .env
echo "DATALAND_TOKEN=your_real_token" > .env

# 2. Run Notebook
jupyter notebook mvp_pipeline.ipynb

# 3. Analyze
cat raw/company_lookup_api.jsonl | jq '.status'
cat raw/company_lookup_documents.jsonl | jq '.status'

# 4. Find successful endpoint
grep '"status":200' raw/company_lookup_*.jsonl
```

## Swagger-Recherche

### API-Service
**URL:** https://dataland.com/api/swagger-ui/index.html

**Gefunden:**
- ✅ `/metadata/available-data-dimensions` - Dimensionen abrufen
- ❌ `/metadata/companies/search` - NICHT dokumentiert

### Documents-Service
**URL:** https://dataland.com/documents/swagger-ui/index.html

**Gefunden:**
- ✅ Document-Operationen (exists, update, extend)
- ❌ Expliziter Company-Search - NICHT dokumentiert

**→ Fazit:** Probing-Ansatz ist notwendig, da kein offizieller Endpoint existiert!

## Next Steps

1. **Test mit echtem Token:** Führe Notebook aus
2. **Identifiziere Endpoint:** Analysiere `raw/*.jsonl` Logs
3. **Optimiere CONFIG:** Behalte nur funktionierende Endpoints
4. **Transform-Layer:** Implementiere JSONL → Events Konvertierung
5. **Mock-Rooms:** Erstelle Mock-Rooms Schema
6. **AI/Q&A:** Nutze Daten für natürlichsprachige Queries

## Support

Bei Problemen:
1. Prüfe `.env` (Token vorhanden?)
2. Prüfe `raw/company_lookup_*.jsonl` (welche Endpoints getestet?)
3. Prüfe Netzwerk (Firewall, VPN, Proxy?)
4. Aktiviere Mock-Modus für Offline-Entwicklung
