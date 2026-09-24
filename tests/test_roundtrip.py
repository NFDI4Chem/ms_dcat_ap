"""Tests for round-tripping schema YAML test data through Python models across profiles.

Reads test data files for each configured profile (legacy, level1), dynamically
instantiates their corresponding Python models, dumps them back to YAML, and
verifies that the round-tripped content matches the original data.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from tests.profiles import LEGACY_PROFILE, LEVEL1_PROFILE, PROFILES, ProfileConfig


def _resolve_class_name(file_path: Path) -> str:
    """Extract LinkML class name from a filename adhering to ClassName-###.yaml."""
    return file_path.stem.split("-")[0]


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.name)
def test_profile_directories_exist(profile: ProfileConfig) -> None:
    """Ensure that the data directory structure exists for each profile."""
    assert profile.valid_dir.is_dir(), f"Missing valid directory for profile {profile.name}: {profile.valid_dir}"
    assert profile.invalid_dir.is_dir(), f"Missing invalid directory for profile {profile.name}: {profile.invalid_dir}"


# Collect all (profile, yaml_file) pairs for parameterized testing
_PROFILE_VALID_FILES = [
    (profile, yaml_file)
    for profile in PROFILES
    for yaml_file in profile.get_valid_files()
]


@pytest.mark.parametrize(
    ("profile", "yaml_file"),
    _PROFILE_VALID_FILES,
    ids=[f"{p.name}:{f.name}" for p, f in _PROFILE_VALID_FILES],
)
def test_pydantic_roundtrip_yaml(profile: ProfileConfig, yaml_file: Path) -> None:
    """Test loading YAML into a profile's Pydantic model, dumping to YAML, and comparing."""
    class_name = _resolve_class_name(yaml_file)
    assert hasattr(
        profile.model, class_name
    ), f"Class {class_name} not found in model for profile {profile.name}"

    model_cls = getattr(profile.model, class_name)

    # 1. Read original YAML data
    with open(yaml_file, encoding="utf-8") as f:
        original_data = yaml.safe_load(f)

    assert isinstance(original_data, dict), f"Expected YAML dict in {yaml_file}"

    # 2. Instantiate Python Pydantic class
    instance = model_cls(**original_data)

    # 3. Dump the class back to YAML
    dumped_dict = instance.model_dump(exclude_none=True, mode="json")
    dumped_yaml_str = yaml.dump(dumped_dict, sort_keys=False)

    # 4. Re-read the dumped YAML and compare with original
    reloaded_data = yaml.safe_load(dumped_yaml_str)

    # Semantic equality check
    assert (
        reloaded_data == original_data
    ), f"Round-trip mismatch for {profile.name}/{yaml_file.name}:\nOriginal: {original_data}\nReloaded: {reloaded_data}"


def test_cross_profile_level1_conforms_to_legacy() -> None:
    """Every valid Level 1 file must also be parseable by the lenient legacy model."""
    valid_files = LEVEL1_PROFILE.get_valid_files()
    if not valid_files:
        pytest.skip("No Level 1 valid files present yet.")
    for yaml_file in valid_files:
        class_name = _resolve_class_name(yaml_file)
        model_cls = getattr(LEGACY_PROFILE.model, class_name)
        with open(yaml_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        instance = model_cls(**data)
        assert instance.id == data["id"]
