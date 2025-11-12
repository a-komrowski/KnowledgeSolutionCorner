from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from ..persist import append_jsonl, create_envelope, nowz


def create_mock_data_if_needed(
    company_info: Optional[Dict[str, Any]],
    dimensions: Optional[List[Dict[str, Any]]],
    values_stats: Optional[Dict[str, Any]],
    documents: Optional[List[Dict[str, Any]]],
    raw_dir: Path,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Dict[str, Any], List[Dict[str, Any]]]:
    """
    Erstellt Mock-Daten, falls keine echten Daten abgerufen oder erfolgreich geladen wurden.

    Diese Funktion wird verwendet, um Test- oder Fallback-Daten zu erzeugen,
    wenn der eigentliche API-/Documents-Abruf keine Ergebnisse liefert.
    Die erzeugten Daten orientieren sich an typischen ESG-Kennzahlen
    (CO₂, Energie, Wasser, Abfall, etc.) und Siemens als Beispielunternehmen.

    Verhalten:
        - Falls keine `company_info` vorhanden ist, wird ein Mock-Unternehmen erzeugt.
        - Falls keine `dimensions` existieren, wird eine Standardliste von Indikatoren erstellt.
        - Falls `values_stats` fehlt oder keine erfolgreichen Werte enthält,
          wird eine JSONL-Datei mit Beispielwerten erzeugt und persistiert.
        - Falls keine `documents` vorhanden sind, werden zwei Beispielberichte
          hinzugefügt und als JSONL gespeichert.

    Args:
        company_info: Informationen über das gefundene Unternehmen oder None.
        dimensions:   Liste der Dimensionsobjekte oder None.
        values_stats: Ergebnisstatistik aus `fetch_all_values()` oder None.
        documents:    Gefundene Dokumente oder None.
        raw_dir:      Zielverzeichnis für die Speicherung der Mock-Dateien.

    Returns:
        Tuple mit vier Elementen:
            (company_info, dimensions, values_stats, documents)
        — jeweils mit echten oder generierten Werten.
    """
    need_mock = (
        company_info is None
        or dimensions is None
        or (values_stats is None)
        or (values_stats and values_stats.get("success", 0) == 0)
    )
    if not need_mock:
        return company_info, dimensions, values_stats, documents

    # --- Mock: Company Info ---
    if company_info is None:
        company_info = {
            "company_id": "mock_siemens_001",
            "name": "Siemens AG (Mock)",
            "sector": "Industrials",
            "country": "Germany",
        }

    # --- Mock: Dimensions ---
    if dimensions is None:
        dimensions = [
            {"dataPointId": "co2_scope1_2023", "indicator": "CO2_Scope1", "period": "2023", "unit": "Mt"},
            {"dataPointId": "co2_scope2_2023", "indicator": "CO2_Scope2", "period": "2023", "unit": "Mt"},
            {"dataPointId": "energy_2023", "indicator": "Energy_Consumption", "period": "2023", "unit": "TWh"},
            {"dataPointId": "renewable_2023", "indicator": "Renewable_Energy_Share", "period": "2023", "unit": "%"},
            {"dataPointId": "water_2023", "indicator": "Water_Consumption", "period": "2023", "unit": "Mio. m³"},
            {"dataPointId": "waste_2023", "indicator": "Waste_Recycling_Rate", "period": "2023", "unit": "%"},
        ]

    # --- Mock: Values ---
    if values_stats is None or values_stats.get("success", 0) == 0:
        values_file = raw_dir / f"values_mock_{nowz().replace(':','').replace('-','').replace('Z','')}.jsonl"
        for val in [
            {"dataPointId": "co2_scope1_2023", "value": 1.24, "unit": "Mt", "quality": "verified"},
            {"dataPointId": "co2_scope2_2023", "value": 0.86, "unit": "Mt", "quality": "verified"},
            {"dataPointId": "energy_2023", "value": 4.5, "unit": "TWh", "quality": "verified"},
            {"dataPointId": "renewable_2023", "value": 70, "unit": "%", "quality": "estimated"},
            {"dataPointId": "water_2023", "value": 3.2, "unit": "Mio. m³", "quality": "verified"},
            {"dataPointId": "waste_2023", "value": 78, "unit": "%", "quality": "verified"},
        ]:
            append_jsonl(
                values_file,
                create_envelope("/data-points/values", 200, {"dataPointId": val["dataPointId"]}, val),
            )
        values_stats = {
            "total": 6,
            "success": 6,
            "failed": 0,
            "skipped_duplicates": 0,
            "errors": [],
            "outfile": str(values_file),
        }

    # --- Mock: Documents ---
    if documents is None:
        documents = [
            {
                "documentId": "doc_2023_sus",
                "title": "Sustainability Report 2023",
                "year": 2023,
                "documentType": "SustainabilityReport",
                "url": "https://example.com/siemens_sus_2023.pdf",
            },
            {
                "documentId": "doc_2022_sus",
                "title": "Sustainability Report 2022",
                "year": 2022,
                "documentType": "SustainabilityReport",
                "url": "https://example.com/siemens_sus_2022.pdf",
            },
        ]
        append_jsonl(
            raw_dir / "document_search.jsonl",
            create_envelope("/documents/search", 200, {"q": "Siemens"}, {"documents": documents}),
        )

    return company_info, dimensions, values_stats, documents
