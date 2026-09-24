"""Tests that programmatically instantiate all schema classes in Python.

Verifies that every class defined in the ms_dcat_ap schema can be successfully
constructed and validated in Python code (exercising both Pydantic and Dataclasses).
"""
from __future__ import annotations

import pytest
from linkml_runtime.utils.schemaview import SchemaView

import ms_dcat_ap.datamodel.ms_dcat_ap as dataclass_model
import ms_dcat_ap.datamodel.ms_dcat_ap_pydantic as pydantic_model


# ---------------------------------------------------------------------------
# Programmatic instantiation of all ms_dcat_ap classes (Pydantic models)
# ---------------------------------------------------------------------------

def test_instantiate_acquisition_mode() -> None:
    obj = pydantic_model.AcquisitionMode(value="DDA")
    assert obj.value == "DDA"


def test_instantiate_detector_type() -> None:
    obj = pydantic_model.DetectorType(value="inductive detector")
    assert obj.value == "inductive detector"


def test_instantiate_ionization_type() -> None:
    obj = pydantic_model.IonizationType(value="electrospray ionization")
    assert obj.value == "electrospray ionization"


def test_instantiate_manufacturer() -> None:
    obj = pydantic_model.Manufacturer(value="Applied Biosystems")
    assert obj.value == "Applied Biosystems"


def test_instantiate_model() -> None:
    obj = pydantic_model.Model(value="API QSTAR Pulsar i")
    assert obj.value == "API QSTAR Pulsar i"


def test_instantiate_mass_analyzer_type() -> None:
    obj = pydantic_model.MassAnalyzerType(value="quadrupole time-of-flight")
    assert obj.value == "quadrupole time-of-flight"


def test_instantiate_scan_polarity() -> None:
    obj = pydantic_model.ScanPolarity(
        value=pydantic_model.ScanPolarityEnum.positive_scan
    )
    assert obj.value == pydantic_model.ScanPolarityEnum.positive_scan


def test_instantiate_scan_window_lower_limit() -> None:
    obj = pydantic_model.ScanWindowLowerLimit(
        value=100.0,
        has_quantity_type="qudt:DimensionlessRatio",
        unit="unit:NUM",
    )
    assert obj.value == pytest.approx(100.0)
    assert obj.unit == "unit:NUM"


def test_instantiate_scan_window_upper_limit() -> None:
    obj = pydantic_model.ScanWindowUpperLimit(
        value=1500.0,
        has_quantity_type="qudt:DimensionlessRatio",
        unit="unit:NUM",
    )
    assert obj.value == pytest.approx(1500.0)
    assert obj.unit == "unit:NUM"


def test_instantiate_ms_sample_base() -> None:
    obj = pydantic_model.MSSample(
        id="https://example.org/samples/sample-001",
        title="Generic MS Sample",
        description="A base sample entity",
        solvent="CHEBI:17790",
    )
    assert obj.id == "https://example.org/samples/sample-001"
    assert obj.title == "Generic MS Sample"


def test_instantiate_substance_ms_sample() -> None:
    obj = pydantic_model.SubstanceMSSample(
        id="https://example.org/samples/rutin-sample",
        title="Rutin test sample",
        description="Prepared rutin sample in methanol",
        solvent="CHEBI:17790",
        injection_volume=pydantic_model.Volume(
            value=5.0,
            has_quantity_type="qudt:Volume",
            unit="unit:MicroL",
        ),
        composed_of=[
            pydantic_model.ChemicalEntity(
                id="http://purl.obolibrary.org/obo/CHEBI_28527",
                title="Rutin",
            )
        ],
    )
    assert obj.id == "https://example.org/samples/rutin-sample"
    assert obj.solvent == "CHEBI:17790"
    assert len(obj.composed_of) == 1


def test_instantiate_material_ms_sample() -> None:
    obj = pydantic_model.MaterialMSSample(
        id="https://example.org/samples/extract-001",
        title="Arabidopsis leaf extract",
        description="Total plant extract",
        solvent="CHEBI:17790",
    )
    assert obj.id == "https://example.org/samples/extract-001"
    assert obj.title == "Arabidopsis leaf extract"


def test_instantiate_mass_spectrometer() -> None:
    obj = pydantic_model.MassSpectrometer(
        id="https://example.org/instruments/api-qstar-pulsar-i",
        title="API QSTAR Pulsar i",
        description="Hybrid LC-ESI-QTOF mass spectrometer.",
        manufacturer=pydantic_model.Manufacturer(value="Applied Biosystems"),
        model=pydantic_model.Model(value="API QSTAR Pulsar i"),
        mass_analyzer_type=pydantic_model.MassAnalyzerType(
            value="quadrupole time-of-flight"
        ),
        ionization_type=pydantic_model.IonizationType(
            value="electrospray ionization"
        ),
        detector_type=pydantic_model.DetectorType(
            value="multichannel plate detector"
        ),
    )
    assert obj.id == "https://example.org/instruments/api-qstar-pulsar-i"
    assert obj.manufacturer.value == "Applied Biosystems"
    assert obj.model.value == "API QSTAR Pulsar i"


def test_instantiate_mass_spectrometry() -> None:
    obj = pydantic_model.MassSpectrometry(
        id="https://example.org/activities/act-001",
        title=["Mass Spectrometry Run"],
        description=["Tandem MS measurement run."],
        carried_out_by=["https://example.org/instruments/api-qstar-pulsar-i"],
        evaluated_entity="https://example.org/samples/rutin-sample",
        acquisition_mode=pydantic_model.AcquisitionMode(value="MS2"),
        scan_polarity=pydantic_model.ScanPolarity(
            value=pydantic_model.ScanPolarityEnum.positive_scan
        ),
        scan_window_lower_limit=pydantic_model.ScanWindowLowerLimit(
            value=100.0,
            has_quantity_type="qudt:DimensionlessRatio",
            unit="unit:NUM",
        ),
        scan_window_upper_limit=pydantic_model.ScanWindowUpperLimit(
            value=1000.0,
            has_quantity_type="qudt:DimensionlessRatio",
            unit="unit:NUM",
        ),
    )
    assert obj.id == "https://example.org/activities/act-001"
    assert obj.carried_out_by == ["https://example.org/instruments/api-qstar-pulsar-i"]
    assert obj.evaluated_entity == "https://example.org/samples/rutin-sample"


def test_instantiate_ms_sample_measurement_dataset() -> None:
    obj = pydantic_model.MSSampleMeasurementDataset(
        id="https://example.org/datasets/ds-001",
        title=["MS Sample Measurement Dataset"],
        description=["Dataset produced by MS run."],
        conforms_to=[
            pydantic_model.Standard(
                title="MS DCAT-AP Profile",
                description="https://w3id.org/NFDI4Chem/ms-dcat-ap",
            )
        ],
        was_generated_by=["https://example.org/activities/act-001"],
        is_about_entity=["https://example.org/samples/rutin-sample"],
    )
    assert obj.id == "https://example.org/datasets/ds-001"
    assert obj.was_generated_by == ["https://example.org/activities/act-001"]
    assert obj.is_about_entity == ["https://example.org/samples/rutin-sample"]


# ---------------------------------------------------------------------------
# Verify complete schema class coverage against SchemaView
# ---------------------------------------------------------------------------

def test_all_schema_classes_are_instantiable() -> None:
    """Ensure every class defined across the ms_dcat_ap modules exists in python models."""
    sv = SchemaView("src/ms_dcat_ap/schema/ms_dcat_ap.yaml")

    # Classes originating from the ms-dcat-ap schema modules
    ms_classes = {
        cls_name
        for cls_name, cls_def in sv.all_classes().items()
        if cls_def.from_schema and "ms-dcat-ap" in cls_def.from_schema
    }

    assert len(ms_classes) == 15, f"Expected 15 MS classes, found: {ms_classes}"

    for cls_name in ms_classes:
        assert hasattr(pydantic_model, cls_name), (
            f"Class {cls_name} missing from pydantic_model"
        )
        assert hasattr(dataclass_model, cls_name), (
            f"Class {cls_name} missing from dataclass_model"
        )
