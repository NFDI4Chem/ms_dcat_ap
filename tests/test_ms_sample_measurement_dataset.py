"""Tests that instantiate an MSSampleMeasurementDataset programmatically.

This exercises the generated pydantic data model and serves as a usage
example for downstream consumers of the schema.
"""
from __future__ import annotations

import pytest

from ms_dcat_ap.datamodel.ms_dcat_ap_pydantic import (
    AcquisitionMode,
    DetectorType,
    IonizationType,
    Manufacturer,
    MassAnalyzerType,
    MassSpectrometer,
    MassSpectrometry,
    MaterialMSSample,
    Model,
    MSSampleMeasurementDataset,
    ScanPolarity,
    ScanPolarityEnum,
    ScanWindowLowerLimit,
    ScanWindowUpperLimit,
    Volume,
)


SAMPLE_IRI = "https://example.org/ms-dcat-ap/samples/caffeine-std-10uM"
INSTRUMENT_IRI = "https://example.org/ms-dcat-ap/instruments/qexactive-001"
ACTIVITY_IRI = "https://example.org/ms-dcat-ap/activities/caffeine-msrun-001"
DATASET_IRI = "https://example.org/ms-dcat-ap/datasets/caffeine-001"


def _build_sample() -> MaterialMSSample:
    """Construct a minimal MaterialMSSample.

    The pydantic model requires nested objects (not URI references) for
    ``evaluated_entity`` / ``is_about_entity`` because their ``any_of``
    constraint resolves to a Union of concrete classes.
    """
    return MaterialMSSample(
        id=SAMPLE_IRI,
        solvent="CHEBI:17790",  # methanol
        injection_volume=Volume(
            value=5.0,
            has_quantity_type="qudt:Volume",
            unit="unit:MicroL",
        ),
    )


def _build_instrument() -> MassSpectrometer:
    """Construct a fully populated MassSpectrometer."""
    return MassSpectrometer(
        id=INSTRUMENT_IRI,
        manufacturer=Manufacturer(value="Thermo Fisher Scientific"),
        model=Model(value="Q Exactive"),
        mass_analyzer_type=MassAnalyzerType(value="orbitrap"),
        ionization_type=IonizationType(value="electrospray ionization"),
        detector_type=DetectorType(value="inductive detector"),
    )


def _build_activity() -> MassSpectrometry:
    """Construct the MassSpectrometry activity that produced the dataset."""
    return MassSpectrometry(
        id=ACTIVITY_IRI,
        carried_out_by=[_build_instrument()],
        evaluated_entity=[_build_sample()],
        acquisition_mode=AcquisitionMode(value="DDA"),
        scan_polarity=ScanPolarity(value=ScanPolarityEnum.positive_scan),
        scan_window_lower_limit=ScanWindowLowerLimit(
            value=100.0,
            has_quantity_type="qudt:DimensionlessRatio",
            unit="unit:NUM",
        ),
        scan_window_upper_limit=ScanWindowUpperLimit(
            value=1500.0,
            has_quantity_type="qudt:DimensionlessRatio",
            unit="unit:NUM",
        ),
    )


def _build_dataset() -> MSSampleMeasurementDataset:
    """Construct the full MSSampleMeasurementDataset."""
    return MSSampleMeasurementDataset(
        id=DATASET_IRI,
        title=["MS measurement of a 10 uM caffeine standard solution"],
        description=[
            "Positive-mode ESI mass spectrum of a 10 uM caffeine standard "
            "solution measured on a Thermo Q-Exactive Orbitrap."
        ],
        was_generated_by=[_build_activity()],
        is_about_entity=[_build_sample()],
    )


def test_instantiate_ms_sample_measurement_dataset() -> None:
    """A fully populated MSSampleMeasurementDataset can be instantiated."""
    ds = _build_dataset()

    # Top-level dataset metadata
    assert ds.id == DATASET_IRI
    assert ds.title == ["MS measurement of a 10 uM caffeine standard solution"]
    assert len(ds.description) == 1
    assert len(ds.is_about_entity) == 1
    assert ds.is_about_entity[0].id == SAMPLE_IRI

    # Provenance: exactly one MassSpectrometry activity
    assert len(ds.was_generated_by) == 1
    activity = ds.was_generated_by[0]
    assert isinstance(activity, MassSpectrometry)
    assert activity.id == ACTIVITY_IRI
    assert len(activity.evaluated_entity) == 1
    assert activity.evaluated_entity[0].id == SAMPLE_IRI

    # Acquisition parameters
    assert activity.acquisition_mode.value == "DDA"
    assert activity.scan_polarity.value == ScanPolarityEnum.positive_scan
    assert activity.scan_window_lower_limit.value == pytest.approx(100.0)
    assert activity.scan_window_upper_limit.value == pytest.approx(1500.0)

    # Instrument used in this run
    assert len(activity.carried_out_by) == 1
    instrument = activity.carried_out_by[0]
    assert isinstance(instrument, MassSpectrometer)
    assert instrument.id == INSTRUMENT_IRI
    assert instrument.manufacturer.value == "Thermo Fisher Scientific"
    assert instrument.model.value == "Q Exactive"
    assert instrument.mass_analyzer_type.value == "orbitrap"
    assert instrument.ionization_type.value == "electrospray ionization"
    assert instrument.detector_type is not None
    assert instrument.detector_type.value == "inductive detector"


def test_dataset_round_trips_to_dict() -> None:
    """The instantiated dataset can be serialised to a plain Python dict."""
    ds = _build_dataset()
    dumped = ds.model_dump(exclude_none=True)

    assert dumped["id"] == DATASET_IRI
    assert dumped["was_generated_by"][0]["acquisition_mode"]["value"] == "DDA"
    assert (
        dumped["was_generated_by"][0]["scan_window_upper_limit"]["unit"]
        == "unit:NUM"
    )
    assert dumped["is_about_entity"][0]["id"] == SAMPLE_IRI


def test_missing_required_field_raises() -> None:
    """Omitting a required field must raise a validation error."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        MSSampleMeasurementDataset(  # type: ignore[call-arg]
            id=DATASET_IRI,
            title=["x"],
            description=["y"],
            # was_generated_by missing on purpose
            is_about_entity=[_build_sample()],
        )

