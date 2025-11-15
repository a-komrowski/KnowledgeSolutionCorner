# Dataland API – genutzte Endpunkte (Beispiel: Siemens Aktiengesellschaft)

**Beispiel-Firma**

- **Name:** Siemens Aktiengesellschaft  
- **Company ID:** `f16a12ff-714c-4dd1-b141-eb8b0355c833`  
- **ISIN (Aktie):** `DE0007236101`  

---

## 1. Dataland Backend API

### 1.1 `company-data-controller`

---

#### 1.1.1 GET `/api/companies/{companyId}`

**Zweck**  
Abruf der vollständigen Unternehmensinformationen inkl. registrierter Datensätze (Framework-Daten).

**Pfadparameter**

| Name        | Typ     | Pflicht | Beschreibung                                                                 |
|------------|---------|---------|------------------------------------------------------------------------------|
| companyId  | String  | Ja      | Eindeutige Company ID auf Dataland (z. B. Siemens: `f16a12ff-714c-4dd1-b141-eb8b0355c833`). |

**Query-Parameter**

- keine

**Swagger-Doku**  
- <https://dataland.com/api/swagger-ui/index.html#/company-data-controller/getCompanyById>

**Beispiel-URL**

```text
https://dataland.com/api/companies/f16a12ff-714c-4dd1-b141-eb8b0355c833
```

**Beispiel-Response**

```json
{
  "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
  "companyInformation": {
    "companyName": "Siemens Aktiengesellschaft",
    "companyAlternativeNames": [
      "Siemens",
      "Siemens AG",
      "SIEMENS AG",
      "Siemens Aktiengesellschaft",
      "Siemens bestaat in Nederland sinds 1879",
      "Siemens & Halske"
    ],
    "companyContactDetails": [],
    "companyLegalForm": null,
    "headquarters": "München",
    "headquartersPostalCode": "80333",
    "fiscalYearEnd": "2024-09-30",
    "reportingPeriodShift": 0,
    "sector": "Industrials",
    "sectorCodeWz": null,
    "identifiers": {
      "Lei": [
        "W38RGI023J3WT1HWRP32"
      ],
      "Isin": [
        "DE0007236101",
        "DE0007236150",
        "DE0007236168",
        "US8261975010"
      ],
      "PermId": [
        "4295869238"
      ],
      "Ticker": [
        "SIE"
      ],
      "Duns": [],
      "CompanyRegistrationNumber": [],
      "VatNumber": []
    },
    "countryCode": "DE",
    "isTeaserCompany": false,
    "website": "https://www.siemens.com/",
    "parentCompanyLei": null,
    "associatedSubdomains": []
  },
  "dataRegisteredByDataland": [
    {
      "dataId": "044d620f-cfa6-4b4c-9da6-9261bbb06a96",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "eutaxonomy-non-financials",
      "uploaderUserId": "136a9394-4873-4a61-a25b-65b1e8e7cc2f",
      "uploadTime": 1693559099929,
      "reportingPeriod": "2021",
      "currentlyActive": false,
      "qaStatus": "Rejected",
      "ref": null
    },
    {
      "dataId": "1a7b5f98-c58f-4168-8e05-78b3924a4767",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "sfdr",
      "uploaderUserId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
      "uploadTime": 1739792623945,
      "reportingPeriod": "2023",
      "currentlyActive": true,
      "qaStatus": "Accepted",
      "ref": null
    },
    {
      "dataId": "34c7b560-0134-493d-aff7-b7e60fc390be",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "sfdr",
      "uploaderUserId": "e5293863-9cab-4aaf-a120-d8934beda96f",
      "uploadTime": 1739781552148,
      "reportingPeriod": "2023",
      "currentlyActive": false,
      "qaStatus": "Accepted",
      "ref": null
    },
    {
      "dataId": "37d00037-f003-4b1c-99a7-18a07cedc4d3",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "sfdr",
      "uploaderUserId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
      "uploadTime": 1733231903813,
      "reportingPeriod": "2023",
      "currentlyActive": false,
      "qaStatus": "Rejected",
      "ref": null
    },
    {
      "dataId": "3c068d31-3307-4705-b35b-017a4f740cc9",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "nuclear-and-gas",
      "uploaderUserId": "e5293863-9cab-4aaf-a120-d8934beda96f",
      "uploadTime": 1740739014010,
      "reportingPeriod": "2024",
      "currentlyActive": true,
      "qaStatus": "Accepted",
      "ref": null
    },
    {
      "dataId": "419ff80a-752c-465a-acf2-5061c2128808",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "eutaxonomy-non-financials",
      "uploaderUserId": "da8cec4c-afa8-48b4-8b0a-8bbef9d11d25",
      "uploadTime": 1705911908490,
      "reportingPeriod": "2022",
      "currentlyActive": true,
      "qaStatus": "Accepted",
      "ref": null
    },
    {
      "dataId": "852a79fc-c34f-4d82-a631-3b026ef7ada1",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "sfdr",
      "uploaderUserId": "156ea265-d6c7-4e5a-86e7-af026cfde3cc",
      "uploadTime": 1733650484211,
      "reportingPeriod": "2023",
      "currentlyActive": false,
      "qaStatus": "Accepted",
      "ref": null
    },
    {
      "dataId": "89ee1283-365e-4776-b67a-166f5b9654ee",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "eutaxonomy-non-financials",
      "uploaderUserId": "e5293863-9cab-4aaf-a120-d8934beda96f",
      "uploadTime": 1732280268835,
      "reportingPeriod": "2023",
      "currentlyActive": false,
      "qaStatus": "Accepted",
      "ref": null
    },
    {
      "dataId": "c408d402-92b8-4fc1-8b4f-b278b95b9514",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "eutaxonomy-non-financials",
      "uploaderUserId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
      "uploadTime": 1732180264169,
      "reportingPeriod": "2023",
      "currentlyActive": false,
      "qaStatus": "Rejected",
      "ref": null
    },
    {
      "dataId": "c729a9f2-559f-41bc-8349-ad1e365389a5",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "eutaxonomy-non-financials",
      "uploaderUserId": "e5293863-9cab-4aaf-a120-d8934beda96f",
      "uploadTime": 1732278928889,
      "reportingPeriod": "2023",
      "currentlyActive": false,
      "qaStatus": "Rejected",
      "ref": null
    },
    {
      "dataId": "d3cda2e2-64aa-43cf-91d8-ce7263d7f68c",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "eutaxonomy-non-financials",
      "uploaderUserId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
      "uploadTime": 1740640754226,
      "reportingPeriod": "2024",
      "currentlyActive": false,
      "qaStatus": "Rejected",
      "ref": null
    },
    {
      "dataId": "d3eabbf2-b663-4455-980b-6ad715400d40",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "eutaxonomy-non-financials",
      "uploaderUserId": "136a9394-4873-4a61-a25b-65b1e8e7cc2f",
      "uploadTime": 1687430784270,
      "reportingPeriod": "2021",
      "currentlyActive": false,
      "qaStatus": "Rejected",
      "ref": null
    },
    {
      "dataId": "dafb237e-9efe-4833-a0bb-1c864d44e25c",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "eutaxonomy-non-financials",
      "uploaderUserId": "da8cec4c-afa8-48b4-8b0a-8bbef9d11d25",
      "uploadTime": 1691160747556,
      "reportingPeriod": "2021",
      "currentlyActive": false,
      "qaStatus": "Rejected",
      "ref": null
    },
    {
      "dataId": "e2ecabe3-1567-4a6c-ba61-205f447b06c1",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "sfdr",
      "uploaderUserId": "320754e5-0c0c-452f-81f6-72f4974db628",
      "uploadTime": 1753779295381,
      "reportingPeriod": "2024",
      "currentlyActive": true,
      "qaStatus": "Accepted",
      "ref": null
    },
    {
      "dataId": "e4db7656-2411-4302-a755-f289ae18ca7b",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "eutaxonomy-non-financials",
      "uploaderUserId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
      "uploadTime": 1739812411644,
      "reportingPeriod": "2023",
      "currentlyActive": true,
      "qaStatus": "Accepted",
      "ref": null
    },
    {
      "dataId": "e85ae4ff-354e-460a-8a4d-bab194c32f15",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "eutaxonomy-non-financials",
      "uploaderUserId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
      "uploadTime": 1740661160040,
      "reportingPeriod": "2024",
      "currentlyActive": true,
      "qaStatus": "Accepted",
      "ref": null
    },
    {
      "dataId": "ff3b21b4-5581-4508-a21d-7603207cd812",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "eutaxonomy-non-financials",
      "uploaderUserId": "da8cec4c-afa8-48b4-8b0a-8bbef9d11d25",
      "uploadTime": 1705663686008,
      "reportingPeriod": "2022",
      "currentlyActive": false,
      "qaStatus": "Accepted",
      "ref": null
    }
  ]
}
```

---

#### 1.1.2 GET `/api/companies/{companyId}/info`

**Zweck**  
Abruf der **reinen** Unternehmensstammdaten (ohne Liste der Datensätze).

**Pfadparameter**

| Name       | Typ    | Pflicht | Beschreibung                    |
|-----------|--------|---------|---------------------------------|
| companyId | String | Ja      | Eindeutige Company ID bei Dataland |

**Query-Parameter**

- keine

**Swagger-Doku**  
- <https://dataland.com/api/swagger-ui/index.html#/company-data-controller/getCompanyInfo>

**Beispiel-URL**

```text
https://dataland.com/api/companies/f16a12ff-714c-4dd1-b141-eb8b0355c833/info
```

**Beispiel-Response (gekürzt)**

```json
{
  "companyName": "Siemens Aktiengesellschaft",
  "companyAlternativeNames": [
    "Siemens",
    "Siemens AG",
    "SIEMENS AG",
    "Siemens Aktiengesellschaft",
    "Siemens bestaat in Nederland sinds 1879",
    "Siemens & Halske"
  ],
  "companyContactDetails": [],
  "companyLegalForm": null,
  "headquarters": "München",
  "headquartersPostalCode": "80333",
  "fiscalYearEnd": "2024-09-30",
  "reportingPeriodShift": 0,
  "sector": "Industrials",
  "sectorCodeWz": null,
  "identifiers": {
    "Lei": ["W38RGI023J3WT1HWRP32"],
    "Isin": [
      "DE0007236101",
      "DE0007236150",
      "DE0007236168",
      "US8261975010"
    ],
    "PermId": ["4295869238"],
    "Ticker": ["SIE"],
    "Duns": [],
    "CompanyRegistrationNumber": [],
    "VatNumber": []
  },
  "countryCode": "DE",
  "isTeaserCompany": false,
  "website": "https://www.siemens.com/",
  "parentCompanyLei": null,
  "associatedSubdomains": []
}
```

---

#### 1.1.3 GET `/api/companies/{companyId}/aggregated-framework-data-summary`

**Zweck**  
Liefert für jedes Reporting-Framework die **Anzahl vorhandener Reporting-Perioden**.

**Pfadparameter**

| Name       | Typ    | Pflicht | Beschreibung                    |
|-----------|--------|---------|---------------------------------|
| companyId | String | Ja      | Eindeutige Company ID bei Dataland |

**Query-Parameter**

- keine

**Swagger-Doku**  
- <https://dataland.com/api/swagger-ui/index.html#/company-data-controller/getAggregatedFrameworkDataSummary>

**Beispiel-URL**

```text
https://dataland.com/api/companies/f16a12ff-714c-4dd1-b141-eb8b0355c833/aggregated-framework-data-summary
```

**Beispiel-Response (gekürzt)**

```json
{
  "sfdr": {
    "numberOfProvidedReportingPeriods": 2
  },
  "eutaxonomy-financials": {
    "numberOfProvidedReportingPeriods": 0
  },
  "eutaxonomy-non-financials": {
    "numberOfProvidedReportingPeriods": 3
  },
  "nuclear-and-gas": {
    "numberOfProvidedReportingPeriods": 1
  },
  "lksg": {
    "numberOfProvidedReportingPeriods": 0
  },
  "pcaf": {
    "numberOfProvidedReportingPeriods": 2
  },
  "vsme": {
    "numberOfProvidedReportingPeriods": 0
  }
}
```

---

#### 1.1.4 GET `/api/companies/identifiers/{identifierType}/{identifier}`

**Zweck**  
Ermittlung der **Company ID** anhand eines Identifiers (z. B. ISIN, LEI, etc.).

**Pfadparameter**

| Name          | Typ    | Pflicht | Beschreibung                                                     |
|---------------|--------|---------|------------------------------------------------------------------|
| identifierType| String | Ja      | Identifier-Typ, z. B. `Isin`, `Lei`, `Ticker`, etc.             |
| identifier    | String | Ja      | Konkreter Identifier (z. B. ISIN `DE0007236101`).               |

**Query-Parameter**

- keine

**Swagger-Doku**  
- <https://dataland.com/api/swagger-ui/index.html#/company-data-controller/getCompanyIdByIdentifier>

**Beispiel-URL**

```text
https://dataland.com/api/companies/identifiers/Isin/DE0007236101
```

**Beispiel-Response**

```json
{
  "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833"
}
```

---

#### 1.1.5 GET `/api/companies/names`

**Zweck**  
Suche von Unternehmen anhand eines Namens/Identifiers (Substring-Suche), mit Limitierung der Treffer.

**Query-Parameter**

| Name         | Typ    | Pflicht | Beschreibung                                                                                  |
|--------------|--------|---------|-----------------------------------------------------------------------------------------------|
| searchString | String | Ja      | Suchstring (min. 3 Zeichen nach Trimmen), wird gegen Namen und Identifier gematcht.          |
| resultLimit  | Int    | Nein    | Maximale Anzahl der zurückgegebenen Treffer.                                                 |

**Swagger-Doku**  
- <https://dataland.com/api/swagger-ui/index.html#/company-data-controller/getCompaniesBySearchString>

**Beispiel-URL**

```text
https://dataland.com/api/companies/names?searchString=Siemens%20AG&resultLimit=100
```

**Beispiel-Response (gekürzt)**

```json
[
  {
    "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
    "companyName": "Siemens Aktiengesellschaft"
  },
  {
    "companyId": "35e67e24-1ab0-4788-96ce-e352f4fe5293",
    "companyName": "Verein von Belegschaftsaktionären in der Siemens AG, e.V. München"
  }
]
```

---

#### 1.1.6 GET `/api/companies`

**Zweck**  
Suche nach Unternehmen mit **Filterung** (Name/Identifier, `countryCode`, `sector`, verfügbare Framework-Daten, etc.).  
Leistungsintensiv – laut Hinweis: „lädt nur langsam“.

**Query-Parameter (laut Beschreibung – kein konkreter Response im Beispiel)**

- Suchstring zu Firmenname/Identifier  
- `countryCode` (optional)  
- `sector` (optional)  
- Filter bzgl. verfügbarer Framework-Daten (optional)  

**Swagger-Doku**  
- <https://dataland.com/api/swagger-ui/index.html#/company-data-controller/getCompanies>

**Beispiel-Response**  
Nicht explizit im Beispiel angegeben; Aufbau analog zu vereinfachten Firmeninfos (Liste von Objekten mit `companyId`, `companyName`, Basis-Metadaten).

---

### 1.2 `sfdr-data-controller`

---

#### 1.2.1 GET `/api/data/sfdr/companies/{companyId}`

**Zweck**  
Abruf der SFDR-Daten einer Firma (einschließlich Meta-Informationen und inhaltlicher Datenstruktur).

**Pfadparameter**

| Name       | Typ    | Pflicht | Beschreibung                      |
|-----------|--------|---------|-----------------------------------|
| companyId | String | Ja      | Eindeutige Company ID bei Dataland |

**Query-Parameter**

| Name           | Typ     | Pflicht | Beschreibung                                                               |
|----------------|---------|---------|----------------------------------------------------------------------------|
| reportingPeriod| String  | Nein    | Berichtsperiode (z. B. `"2023"`).                                         |
| showOnlyActive | Boolean | Nein    | Wenn `true`, nur aktuell aktive Datensätze; ansonsten alle.               |

**Swagger-Doku**  
- <https://dataland.com/api/swagger-ui/index.html#/sfdr-data-controller/getAllCompanySfdrData>

**Beispiel-URL**

```text
https://dataland.com/api/data/sfdr/companies/f16a12ff-714c-4dd1-b141-eb8b0355c833?showOnlyActive=true&reportingPeriod=2023
```

**Beispiel-Response (stark gekürzt)**

```json
[
  {
    "metaInfo": {
      "dataId": "not available",
      "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
      "dataType": "sfdr",
      "uploaderUserId": null,
      "uploadTime": 1754466296061,
      "reportingPeriod": "2023",
      "currentlyActive": true,
      "qaStatus": "Accepted",
      "ref": null
    },
    "data": {
      "general": {
        "general": {
          "dataDate": "2023-12-04",
          "fiscalYearDeviation": "Deviation",
          "fiscalYearEnd": "2023-09-30",
          "referencedReports": {
            "sustainability-report-fy2023.pdf": {
              "fileReference": "871d8b265a...",
              "fileName": "sustainability-report-fy2023.pdf",
              "publicationDate": null
            }
            // ... weitere Referenzen gekürzt
          }
        }
      },
      "environmental": {
        "greenhouseGasEmissions": {
          "scope1GhgEmissionsInTonnes": {
            "value": 387000,
            "quality": "Reported",
            "comment": "The greenhouse gas emissions for Scope 1 ...",
            "dataSource": {
              "page": "60",
              "fileName": "sustainability-report-fy2023.pdf",
              "fileReference": "871d8b265a...",
              "publicationDate": null
            }
          },
          "scope2GhgEmissionsInTonnes": {
            "value": 624000,
            "quality": "Reported"
            // ... gekürzt
          }
          // ... weitere Emissionsfelder gekürzt
        },
        "energyPerformance": {
          "renewableEnergyConsumptionInGWh": {
            "value": 1293.82,
            "quality": "Estimated"
            // ... gekürzt
          }
          // ... weitere Energiefelder gekürzt
        },
        "biodiversity": {
          "biodiversityProtectionPolicy": {
            "value": "Yes",
            "quality": "Reported"
            // ... gekürzt
          }
          // ... weitere Biodiversitätsfelder gekürzt
        },
        "water": {
          "waterConsumptionInCubicMeters": {
            "value": 510000,
            "quality": "Reported"
            // ... gekürzt
          }
          // ... weitere Wasserfelder gekürzt
        },
        "waste": {
          "hazardousAndRadioactiveWasteInTonnes": {
            "value": 12700,
            "quality": "Reported"
          }
          // ... weitere Abfallfelder gekürzt
        },
        "emissions": {
          "emissionsOfOzoneDepletionSubstancesInTonnes": {
            "value": 0.044,
            "quality": "Reported"
          },
          "carbonReductionInitiatives": {
            "value": "Yes",
            "quality": "Reported"
          }
        }
      },
      "social": {
        "socialAndEmployeeMatters": {
          "iloCoreLabourStandards": {
            "value": "Yes",
            "quality": "Incomplete"
          },
          "policyAgainstChildLabour": {
            "value": "Yes",
            "quality": "Reported"
          },
          "rateOfAccidents": {
            "value": 0.24,
            "quality": "Reported"
          },
          "excessiveCeoPayRatio": {
            "value": 48.94,
            "quality": "Estimated"
          }
          // ... weitere soziale Felder gekürzt
        },
        "humanRights": {
          "humanRightsPolicy": {
            "value": "Yes",
            "quality": "Reported"
          }
          // ... gekürzt
        },
        "antiCorruptionAndAntiBribery": {
          "reportedConvictionsOfBriberyAndCorruption": {
            "value": 0,
            "quality": "Reported"
          }
        }
      }
    }
  }
]
```

**Typische Nutzung**  
- Abruf und Speicherung der SFDR-Daten einer Firma als JSON (z. B. zur Weiterverarbeitung in einer eigenen Anwendung).

---

### 1.3 `meta-data-controller`

---

#### 1.3.1 GET `/api/metadata`

**Zweck**  
Abruf von Meta-Informationen über Datensätze (Framework-Daten) für eine Firma mit verschiedenen Filtern.

**Query-Parameter**

| Name           | Typ     | Pflicht | Beschreibung                                                                                          |
|----------------|---------|---------|-------------------------------------------------------------------------------------------------------|
| companyId      | String  | Ja      | Company ID (z. B. Siemens: `f16a12ff-714c-4dd1-b141-eb8b0355c833`).                                   |
| dataType       | String  | Nein    | Framework / Datentyp (z. B. `sfdr`, `eutaxonomy-non-financials`).                                    |
| showOnlyActive | Boolean | Nein    | Wenn `true` (oder leer), nur aktuell aktive Datensätze. Bei `false` alle Datensätze.                |
| reportingPeriod| String  | Nein    | Berichtsperiode (z. B. `"2023"`).                                                                    |
| qaStatus       | String  | Nein    | QA-Status, z. B. `Pending`, `Accepted`, `Rejected`.                                                  |

**Swagger-Doku**  
- <https://dataland.com/api/swagger-ui/index.html#/meta-data-controller/getListOfDataMetaInfo>

**Beispiel-URL**

```text
https://dataland.com/api/metadata?companyId=f16a12ff-714c-4dd1-b141-eb8b0355c833&showOnlyActive=true&reportingPeriod=2023&qaStatus=Accepted
```

**Beispiel-Response (gekürzt)**

```json
[
  {
    "dataId": "e4db7656-2411-4302-a755-f289ae18ca7b",
    "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
    "dataType": "eutaxonomy-non-financials",
    "uploaderUserId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
    "uploadTime": 1739812411644,
    "reportingPeriod": "2023",
    "currentlyActive": true,
    "qaStatus": "Accepted",
    "ref": "https://dataland.com/companies/f16a12ff-714c-4dd1-b141-eb8b0355c833/frameworks/eutaxonomy-non-financials/e4db7656-2411-4302-a755-f289ae18ca7b"
  },
  {
    "dataId": "1a7b5f98-c58f-4168-8e05-78b3924a4767",
    "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
    "dataType": "sfdr",
    "uploaderUserId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
    "uploadTime": 1739792623945,
    "reportingPeriod": "2023",
    "currentlyActive": true,
    "qaStatus": "Accepted",
    "ref": "https://dataland.com/companies/f16a12ff-714c-4dd1-b141-eb8b0355c833/frameworks/sfdr/1a7b5f98-c58f-4168-8e05-78b3924a4767"
  }
]
```

---

#### 1.3.2 GET `/api/metadata/{dataId}`

**Zweck**  
Abruf der Meta-Informationen zu einem einzelnen Datensatz anhand seiner `dataId`.

**Pfadparameter**

| Name   | Typ    | Pflicht | Beschreibung      |
|--------|--------|---------|-------------------|
| dataId | String | Ja      | ID des Datensatzes |

**Swagger-Doku**  
- (Meta-Doku-Root) <https://dataland.com/api/swagger-ui/index.html#/>

**Beispiel-URL**

```text
https://dataland.com/api/metadata/1a7b5f98-c58f-4168-8e05-78b3924a4767
```

**Beispiel-Response**

```json
{
  "dataId": "1a7b5f98-c58f-4168-8e05-78b3924a4767",
  "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
  "dataType": "sfdr",
  "uploaderUserId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
  "uploadTime": 1739792623945,
  "reportingPeriod": "2023",
  "currentlyActive": true,
  "qaStatus": "Accepted",
  "ref": "https://dataland.com/companies/f16a12ff-714c-4dd1-b141-eb8b0355c833/frameworks/sfdr/1a7b5f98-c58f-4168-8e05-78b3924a4767"
}
```

---

#### 1.3.3 GET `/api/metadata/{dataId}/data-points`

**Zweck**  
Liefert eine Map der **Datenpunkt-Typen** zu ihren **Data-Point-IDs** innerhalb eines Datensatzes.

**Pfadparameter**

| Name   | Typ    | Pflicht | Beschreibung      |
|--------|--------|---------|-------------------|
| dataId | String | Ja      | ID des Datensatzes |

**Swagger-Doku**  
- <https://dataland.com/api/swagger-ui/index.html#/meta-data-controller/getContainedDataPoints>

**Beispiel-URL**

```text
https://dataland.com/api/metadata/1a7b5f98-c58f-4168-8e05-78b3924a4767/data-points
```

**Beispiel-Response (stark gekürzt)**

```json
{
  "extendedDecimalGhgIntensityScope2InTonnesPerMillionEURRevenue": "09b2fd06-5b63-4ab2-8a67-b16b3a3c3072",
  "extendedDecimalNonRecycledWasteInTonnes": "f24c7ac1-f776-4e73-89a2-e0ad06420651",
  "extendedEnumYesNoPolicyAgainstDiscriminationInTheWorkplace": "0bd4b5e9-5910-4a80-9a19-5e71304f0d23",
  "extendedDecimalNonRenewableEnergyConsumptionFossilFuelsInGWh": "1fa415aa-6986-4695-ae15-96b517f81229",
  "extendedDecimalScope3UpstreamGhgEmissionsInTonnes": "1dd88af1-8853-4f22-af89-f0f8f9b06b26",
  "extendedEnumYesNoPolicyAgainstForcedLabour": "8279f216-4066-4dfa-8c7f-a73b4325dc1c",
  "extendedDecimalWaterConsumptionInCubicMeters": "5c2c1967-a44a-488e-9fa8-f8cac1b553fc",
  "extendedDecimalScope1GhgEmissionsInTonnes": "0e6a390a-f885-48cb-b8d6-d67702592be0",
  "extendedDecimalScope1And2And3GhgEmissionsMarketBasedInTonnes": "f87abc9a-3cf2-4586-9a9e-018872b41ad3"
  // ... viele weitere Einträge gekürzt
}
```

---

### 1.4 `data-point-controller`

---

#### 1.4.1 GET `/api/data-points/{dataPointId}`

**Zweck**  
Abruf des Inhalts eines einzelnen Datenpunkts (Wert, Qualität, Kommentar, Datenquelle etc.).

**Pfadparameter**

| Name        | Typ    | Pflicht | Beschreibung                 |
|-------------|--------|---------|------------------------------|
| dataPointId | String | Ja      | ID des Datenpunkts           |

**Swagger-Doku**  
- <https://dataland.com/api/swagger-ui/index.html#/data-point-controller/getDataPointMetaInfo>

**Beispiel-URL**

```text
https://dataland.com/api/data-points/f87abc9a-3cf2-4586-9a9e-018872b41ad3
```

**Beispiel-Response (Scope 1+2+3 GHG, market-based, gekürzt)**

```json
{
  "dataPoint": "{\"value\":483738000,\"quality\":\"Estimated\",\"comment\":\"From the relevant document the sum of Scope 1, 2 (market-based), and 3 greenhouse gas emissions for Siemens Aktiengesellschaft in 2023 can be derived. The total is 483,738 thousand metric tons of CO2 equivalents.\",\"dataSource\":{\"page\":\"107-109\",\"tagName\":null,\"fileName\":\"sustainability-report-fy2023.pdf\",\"fileReference\":\"871d8b265a576e8caf6ff4525ae26a87e939cb8c1b76451658ddb94c64e62fa5\",\"publicationDate\":null}}",
  "dataPointType": "extendedDecimalScope1And2And3GhgEmissionsMarketBasedInTonnes",
  "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
  "reportingPeriod": "2023"
}
```

---

#### 1.4.2 GET `/api/data-points/{dataPointId}/metadata`

**Zweck**  
Abruf der **Meta-Informationen** zu einem Datenpunkt (ohne eingebetteten Wert).

**Pfadparameter**

| Name        | Typ    | Pflicht | Beschreibung                 |
|-------------|--------|---------|------------------------------|
| dataPointId | String | Ja      | ID des Datenpunkts           |

**Swagger-Doku**  
- <https://dataland.com/api/swagger-ui/index.html#/>

**Beispiel-URL**

```text
https://dataland.com/api/data-points/f87abc9a-3cf2-4586-9a9e-018872b41ad3/metadata
```

**Beispiel-Response**

```json
{
  "dataPointId": "f87abc9a-3cf2-4586-9a9e-018872b41ad3",
  "dataPointType": "extendedDecimalScope1And2And3GhgEmissionsMarketBasedInTonnes",
  "companyId": "f16a12ff-714c-4dd1-b141-eb8b0355c833",
  "reportingPeriod": "2023",
  "uploaderUserId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
  "uploadTime": 1739792623945,
  "currentlyActive": true,
  "qaStatus": "Accepted"
}
```

---

## 2. Dataland Document Manager API

### 2.1 `document-controller`

---

#### 2.1.1 GET `/documents`

**Zweck**  
Suche nach Dokument-Metainformationen anhand von Company ID und optional Reporting-Periode (und ggf. Kategorien).  
Ergebnis sortiert nach Publikationsdatum (absteigend). Nur Datensätze mit `qaStatus = Accepted`.

**Query-Parameter**

| Name           | Typ    | Pflicht | Beschreibung                                      |
|----------------|--------|---------|---------------------------------------------------|
| companyId      | String | Ja      | Company ID                                        |
| reportingPeriod| String | Nein    | Berichtsperiode (z. B. `"2023"`)                  |
| documentCategory| String| Nein    | (optional) Filter nach Dokumentkategorie (z. B. `SustainabilityReport`, `AnnualReport`) |

**Swagger-Doku**  
- <https://dataland.com/documents/swagger-ui/index.html#/document-controller/searchForDocumentMetaInformation>

**Beispiel-URL**

```text
https://dataland.com/documents/?companyId=f16a12ff-714c-4dd1-b141-eb8b0355c833&reportingPeriod=2023
```

**Beispiel-Response (gekürzt)**

```json
[
  {
    "documentId": "871d8b265a576e8caf6ff4525ae26a87e939cb8c1b76451658ddb94c64e62fa5",
    "documentName": "sustainability-report-fy2023.pdf",
    "documentCategory": "SustainabilityReport",
    "companyIds": [
      "f16a12ff-714c-4dd1-b141-eb8b0355c833"
    ],
    "uploaderId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
    "publicationDate": null,
    "reportingPeriod": "2023"
  },
  {
    "documentId": "a1bde2b6f7b0408c34ee7188cff4fe42feccd3a886eaf47c05827aa3452969b1",
    "documentName": "Siemens_Report_FY2023.pdf",
    "documentCategory": "AnnualReport",
    "companyIds": [
      "f16a12ff-714c-4dd1-b141-eb8b0355c833"
    ],
    "uploaderId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
    "publicationDate": null,
    "reportingPeriod": "2023"
  }
]
```

**Typische Nutzung**  
- Liste aller relevanten Dokumente einer Firma zu einer Berichtsperiode (z. B. für Download-/Viewer-UI).

---

#### 2.1.2 GET `/documents/{documentId}`

**Zweck**  
Download eines Dokuments anhand seiner `documentId` (z. B. PDF).  
Geeignet für Proxy-Download oder Inline-Anzeige (PDF-Viewer).

**Pfadparameter**

| Name       | Typ    | Pflicht | Beschreibung      |
|------------|--------|---------|-------------------|
| documentId | String | Ja      | ID des Dokuments  |

**Swagger-Doku**  
- <https://dataland.com/documents/swagger-ui/index.html#/document-controller/getDocument>

**Beispiel-URL**

```text
https://dataland.com/documents/871d8b265a576e8caf6ff4525ae26a87e939cb8c1b76451658ddb94c64e62fa5
```

**Beispiel-Response**

- Binärdaten des Dokuments (z. B. PDF-Datei)  
- kein JSON, sondern File-Download

---

#### 2.1.3 GET `/documents/{documentId}/metadata`

**Zweck**  
Abruf der Metainformationen zu einem Dokument (Name, Kategorie, Company IDs, QA-Status etc.).

**Pfadparameter**

| Name       | Typ    | Pflicht | Beschreibung      |
|------------|--------|---------|-------------------|
| documentId | String | Ja      | ID des Dokuments  |

**Swagger-Doku**  
- <https://dataland.com/documents/swagger-ui/index.html#/document-controller/getDocumentMetaInformation>

**Beispiel-URL**

```text
https://dataland.com/documents/871d8b265a576e8caf6ff4525ae26a87e939cb8c1b76451658ddb94c64e62fa5/metadata
```

**Beispiel-Response**

```json
{
  "documentId": "871d8b265a576e8caf6ff4525ae26a87e939cb8c1b76451658ddb94c64e62fa5",
  "documentType": "Pdf",
  "documentName": "sustainability-report-fy2023.pdf",
  "documentCategory": "SustainabilityReport",
  "companyIds": [
    "f16a12ff-714c-4dd1-b141-eb8b0355c833"
  ],
  "uploaderId": "8a4c0912-3fe9-4754-86dc-a0c4ab00d1f6",
  "uploadTime": 1733221825921,
  "publicationDate": null,
  "reportingPeriod": "2023",
  "qaStatus": "Accepted",
  "isViewableByUser": true
}
```

---

## 3. Übersicht: wichtigste Variablen je Use Case

Zum schnellen Nachschlagen:

- **Firma suchen und auswählen**
  - Endpoint: `GET /api/companies/names`
  - Parameter: `searchString` (min. 3 Zeichen), `resultLimit` (optional)

- **Company ID aus ISIN holen**
  - Endpoint: `GET /api/companies/identifiers/{identifierType}/{identifier}`
  - Beispiel: `identifierType = Isin`, `identifier = DE0007236101`

- **Stammdaten einer Firma holen**
  - Endpoint: `GET /api/companies/{companyId}/info`
  - Parameter: `companyId` (Pfad)

- **Verfügbare Framework-Datensätze (Meta-Info)**
  - Endpoint: `GET /api/metadata`
  - Parameter: `companyId`, optional `dataType`, `reportingPeriod`, `showOnlyActive`, `qaStatus`

- **SFDR-Daten einer Firma**
  - Endpoint: `GET /api/data/sfdr/companies/{companyId}`
  - Parameter: `companyId` (Pfad), optional `reportingPeriod`, `showOnlyActive`

- **Einzelnen Datenpunkt holen**
  - Meta-Mapping: `GET /api/metadata/{dataId}/data-points`
  - Inhalt: `GET /api/data-points/{dataPointId}`
  - Meta zum Datenpunkt: `GET /api/data-points/{dataPointId}/metadata`

- **Dokumente der Firma (z. B. Report PDFs)**
  - Liste: `GET /documents?companyId=...&reportingPeriod=...`
  - PDF-Download: `GET /documents/{documentId}`
  - Meta: `GET /documents/{documentId}/metadata`
