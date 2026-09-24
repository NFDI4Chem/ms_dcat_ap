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
    Model,
    MSSampleMeasurementDataset,
    ScanPolarity,
    ScanPolarityEnum,
    ScanWindowLowerLimit,
    ScanWindowUpperLimit,
    Standard,
)


SAMPLE_IRI = "https://example.org/ms-dcat-ap/samples/caffeine-std-10uM"
INSTRUMENT_IRI = "https://example.org/ms-dcat-ap/instruments/qexactive-001"
ACTIVITY_IRI = "https://example.org/ms-dcat-ap/activities/caffeine-msrun-001"
DATASET_IRI = "https://example.org/ms-dcat-ap/datasets/caffeine-001"


def _sample_ref() -> str:
    """Return the IRI reference to the sample described elsewhere."""
    return SAMPLE_IRI


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
        carried_out_by=[INSTRUMENT_IRI],
        evaluated_entity=_sample_ref(),
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
        conforms_to=[
            Standard(
                title="MIChI MS Level 1 Profile",
                description="https://w3id.org/NFDI4Chem/ms-dcat-ap/profiles/level-1",
            )
        ],
        was_generated_by=[ACTIVITY_IRI],
        is_about_entity=[_sample_ref()],
    )


def test_instantiate_ms_sample_measurement_dataset() -> None:
    """A fully populated MSSampleMeasurementDataset can be instantiated."""
    ds = _build_dataset()

    # Top-level dataset metadata
    assert ds.id == DATASET_IRI
    assert ds.title == ["MS measurement of a 10 uM caffeine standard solution"]
    assert len(ds.description) == 1
    assert ds.is_about_entity == [SAMPLE_IRI]
    assert ds.conforms_to is not None
    assert len(ds.conforms_to) == 1
    assert ds.conforms_to[0].title == "MIChI MS Level 1 Profile"
    assert (
        ds.conforms_to[0].description
        == "https://w3id.org/NFDI4Chem/ms-dcat-ap/profiles/level-1"
    )

    # Provenance: exactly one MassSpectrometry activity IRI
    assert ds.was_generated_by == [ACTIVITY_IRI]

    # Instantiate activity and verify its properties
    activity = _build_activity()
    assert activity.id == ACTIVITY_IRI
    assert activity.evaluated_entity == SAMPLE_IRI

    # Acquisition parameters
    assert activity.acquisition_mode.value == "DDA"
    assert activity.scan_polarity.value == ScanPolarityEnum.positive_scan
    assert activity.scan_window_lower_limit.value == pytest.approx(100.0)
    assert activity.scan_window_upper_limit.value == pytest.approx(1500.0)

    # Instrument reference and instrument properties
    assert activity.carried_out_by == [INSTRUMENT_IRI]
    instrument = _build_instrument()
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
    assert dumped["was_generated_by"] == [ACTIVITY_IRI]
    assert dumped["is_about_entity"] == [SAMPLE_IRI]


def test_instantiate_legacy_minimal_dataset() -> None:
    """A minimal legacy dataset omitting recommended fields can be instantiated."""
    minimal_instrument = MassSpectrometer(
        id=INSTRUMENT_IRI,
        model=Model(value="API QSTAR Pulsar i"),
    )
    minimal_activity = MassSpectrometry(
        id=ACTIVITY_IRI,
        carried_out_by=[INSTRUMENT_IRI],
        evaluated_entity=_sample_ref(),
    )
    minimal_dataset = MSSampleMeasurementDataset(
        id=DATASET_IRI,
        title=["Minimal legacy dataset"],
        description=["Minimal legacy test dataset."],
        conforms_to=[
            Standard(
                title="MS DCAT-AP Profile",
                description="https://w3id.org/NFDI4Chem/ms-dcat-ap",
            )
        ],
        was_generated_by=[ACTIVITY_IRI],
        is_about_entity=[_sample_ref()],
    )

    assert minimal_dataset.id == DATASET_IRI
    assert minimal_dataset.conforms_to is not None
    assert len(minimal_dataset.conforms_to) == 1
    assert minimal_dataset.conforms_to[0].title == "MS DCAT-AP Profile"
    assert len(minimal_dataset.was_generated_by) == 1
    assert minimal_activity.acquisition_mode is None
    assert minimal_activity.scan_polarity is None
    assert minimal_activity.scan_window_lower_limit is None
    assert minimal_instrument.mass_analyzer_type is None
    assert minimal_instrument.ionization_type is None


def test_missing_required_field_raises() -> None:
    """Omitting a required field must raise a validation error."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        MSSampleMeasurementDataset(  # type: ignore[call-arg]
            id=DATASET_IRI,
            title=["x"],
            description=["y"],
            # was_generated_by missing on purpose
            is_about_entity=[_sample_ref()],
        )


def test_level1_pydantic_model_validates_full_dataset() -> None:
    """The strict Level 1 Pydantic model successfully validates a complete dataset."""
    from ms_dcat_ap.datamodel.ms_dcat_ap_level1_pydantic import (
        AcquisitionMode as L1AcquisitionMode,
        DetectorType as L1DetectorType,
        IonizationType as L1IonizationType,
        Manufacturer as L1Manufacturer,
        MassAnalyzerType as L1MassAnalyzerType,
        MassSpectrometer as L1MassSpectrometer,
        MassSpectrometry as L1MassSpectrometry,
        Model as L1Model,
        MSSampleMeasurementDataset as L1MSSampleMeasurementDataset,
        ScanPolarity as L1ScanPolarity,
        ScanPolarityEnum as L1ScanPolarityEnum,
        ScanWindowLowerLimit as L1ScanWindowLowerLimit,
        ScanWindowUpperLimit as L1ScanWindowUpperLimit,
        Standard as L1Standard,
    )

    instrument = L1MassSpectrometer(
        id=INSTRUMENT_IRI,
        manufacturer=L1Manufacturer(value="Thermo Fisher Scientific"),
        model=L1Model(value="Q Exactive"),
        mass_analyzer_type=L1MassAnalyzerType(value="orbitrap"),
        ionization_type=L1IonizationType(value="electrospray ionization"),
        detector_type=L1DetectorType(value="inductive detector"),
    )
    activity = L1MassSpectrometry(
        id=ACTIVITY_IRI,
        carried_out_by=[INSTRUMENT_IRI],
        evaluated_entity=_sample_ref(),
        acquisition_mode=L1AcquisitionMode(value="DDA"),
        scan_polarity=L1ScanPolarity(value=L1ScanPolarityEnum.positive_scan),
        scan_window_lower_limit=L1ScanWindowLowerLimit(
            value=100.0,
            has_quantity_type="qudt:DimensionlessRatio",
            unit="unit:NUM",
        ),
        scan_window_upper_limit=L1ScanWindowUpperLimit(
            value=1500.0,
            has_quantity_type="qudt:DimensionlessRatio",
            unit="unit:NUM",
        ),
    )
    ds = L1MSSampleMeasurementDataset(
        id=DATASET_IRI,
        title=["MS measurement of a 10 uM caffeine standard solution"],
        description=["Level 1 dataset description."],
        conforms_to=[
            L1Standard(
                title="MIChI MS Level 1 Profile",
                description="https://w3id.org/NFDI4Chem/ms-dcat-ap/profiles/level-1",
            )
        ],
        was_generated_by=[ACTIVITY_IRI],
        is_about_entity=[_sample_ref()],
    )

    assert ds.id == DATASET_IRI
    assert len(ds.was_generated_by) == 1
    assert instrument.id == INSTRUMENT_IRI
    assert activity.id == ACTIVITY_IRI


def test_level1_pydantic_model_rejects_missing_recommended_fields() -> None:
    """The strict Level 1 model rejects datasets missing MIChI Level 1 required fields."""
    from pydantic import ValidationError
    from ms_dcat_ap.datamodel.ms_dcat_ap_level1_pydantic import (
        MassSpectrometer as L1MassSpectrometer,
        MassSpectrometry as L1MassSpectrometry,
        Model as L1Model,
    )

    # In Level 1, manufacturer, mass_analyzer_type, ionization_type are required on MassSpectrometer
    with pytest.raises(ValidationError):
        L1MassSpectrometer(
            id=INSTRUMENT_IRI,
            model=L1Model(value="API QSTAR Pulsar i"),
        )

    # In Level 1, acquisition_mode, scan_polarity, scan limits are required on MassSpectrometry
    with pytest.raises(ValidationError):
        L1MassSpectrometry(
            id=ACTIVITY_IRI,
            evaluated_entity=_sample_ref(),
        )


def test_yaml_example_dataset_against_both_models() -> None:
    """Test loading the Rutin YAML example dataset against base and Level 1 models."""
    import yaml
    from ms_dcat_ap.datamodel.ms_dcat_ap_pydantic import (
        MSSampleMeasurementDataset as BaseDataset,
    )
    from ms_dcat_ap.datamodel.ms_dcat_ap_level1_pydantic import (
        MSSampleMeasurementDataset as Level1Dataset,
    )
    from tests.profiles import LEGACY_PROFILE

    with open(LEGACY_PROFILE.valid_dir / "MSSampleMeasurementDataset-001.yaml") as f:
        data_full = yaml.safe_load(f)

    # Rutin dataset parses successfully with BOTH models
    assert BaseDataset(**data_full).id == data_full["id"]
    assert Level1Dataset(**data_full).id == data_full["id"]

