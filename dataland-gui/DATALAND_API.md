# Dataland API – genutzte Endpunkte

## Dataland Backend API documentation

### Companies
- **GET** `/api/companies/names`
  - Query: `searchString`, `resultLimit`
  - Nutzen: Firmen suchen und auswählen.

### SFDR
- **GET** `/api/data/sfdr/companies/{companyId}`
  - Query: `reportingPeriod` (optional), `showOnlyActive` (true/false)
  - Nutzen: SFDR‑Daten einer Firma abrufen und als JSON speichern.

### (Optional) Metadata/Datapoints Explorer
- **GET** `/api/metadata?companyId=...&showOnlyActive=...&reportingPeriod=...&qaStatus=...`
- **GET** `/api/metadata/{dataId}/data-points`
- **GET** `/api/data-points/{dataPointId}`
- **GET** `/api/data-points/{dataPointId}/value`
- **GET** `/api/data-points/{dataPointId}/values`
- **GET** `/api/data-points/{dataPointId}/data`
- **GET** `/api/data-points/{dataPointId}/metadata`
  - Nutzen: Datenpunkte mit Werten identifizieren.

## Dataland Document Manager API documentation

### Documents
- **GET** `/documents`
  - Query: `companyId`, `reportingPeriod` (optional)
  - Nutzen: Dokumente der Firma auflisten.
- **GET** `/documents/{documentId}`
  - Nutzen: Proxy‑Download & Inline‑Anzeige (PDF).