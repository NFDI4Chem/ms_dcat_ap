"""Configuration and utilities for schema profiles (legacy vs. level1) used in tests."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

import ms_dcat_ap.datamodel.ms_dcat_ap_pydantic as legacy_model
import ms_dcat_ap.datamodel.ms_dcat_ap_level1_pydantic as level1_model

DATA_DIR = Path(__file__).parent / "data"


@dataclass(frozen=True)
class ProfileConfig:
    name: str
    model: ModuleType
    valid_dir: Path
    invalid_dir: Path

    def get_valid_files(self) -> list[Path]:
        """Return all valid YAML example files for this profile."""
        if not self.valid_dir.exists():
            return []
        return sorted(self.valid_dir.glob("*.yaml"))

    def get_invalid_files(self) -> list[Path]:
        """Return all counter-example YAML files for this profile."""
        if not self.invalid_dir.exists():
            return []
        return sorted(self.invalid_dir.glob("*.yaml"))


LEGACY_PROFILE = ProfileConfig(
    name="legacy",
    model=legacy_model,
    valid_dir=DATA_DIR / "legacy" / "valid",
    invalid_dir=DATA_DIR / "legacy" / "invalid",
)

LEVEL1_PROFILE = ProfileConfig(
    name="level1",
    model=level1_model,
    valid_dir=DATA_DIR / "level1" / "valid",
    invalid_dir=DATA_DIR / "level1" / "invalid",
)

PROFILES: list[ProfileConfig] = [LEGACY_PROFILE, LEVEL1_PROFILE]
