# AGENTS.md

## Overview

This project implements a domain-specific DCAT-AP profile for mass spectrometry (MS) according to MIChI recommendations. The central data structure is defined as a modular LinkML schema under `src/ms_dcat_ap/schema/`, from which various artifacts (e.g., Python data models for legacy and strict profiles, documentation, validation rules) are generated.

---

## Architecture & Schema Design

### Modular Schema Architecture (`src/ms_dcat_ap/schema/`)
- **Topic-based Modularization:** To keep the schema clean and maintainable, classes, enums, and related slots are organized modularly into separate YAML files by topic or domain concept.
- **Base Profiles & Imports:** Built upon `chem_dcat_ap.yaml` (and upstream DCAT-AP+ / Chemistry profiles).

### Two Profile Schemas: Legacy vs. MIChI Level 1
The project provides two primary schema entry points:
1. **`ms_dcat_ap.yaml` (Legacy / Lenient Profile):**
   - Imports all relevant modular schema components.
   - Designed for legacy datasets: only essential identifiers and core metadata slots are `required: true`. MIChI attributes remain optional or recommended to maintain broad compatibility.
2. **`ms_dcat_ap_level1.yaml` (MIChI Level 1 / Strict Profile):**
   - Imports `ms_dcat_ap.yaml` and enforces strict MIChI Level 1 compliance using `slot_usage`.
   - Makes recommended metadata fields strictly required for current data.

### Generated Artifacts
- **Python Data Models (`src/ms_dcat_ap/datamodel/`):**
  - `ms_dcat_ap.py`: Dataclasses model for the core schema.
  - `ms_dcat_ap_pydantic.py`: Pydantic model for legacy / flexible data.
  - `ms_dcat_ap_level1_pydantic.py`: Pydantic model for strict MIChI Level 1 validated data.
- **Project Artifacts (`project/`):**
  - Generated Java, TypeScript, OWL, and JSON-Schema definitions. **Never edit manually; always regenerate!**
- **Documentation (`docs/`):**
  - Schema documentation is generated into `docs/elements/` and built via MkDocs.

---

## Developer Workflows

- **Command Overview:**
  - Use the [`just`](https://github.com/casey/just) tool for all build, test, and generation tasks.
  - `just` or `just --list` shows all available commands.
- **Typical Workflows:**
  - **Generate artifacts:**
    - `just gen-project` (generates all project artifacts and both Pydantic models: `ms_dcat_ap_pydantic.py` and `ms_dcat_ap_level1_pydantic.py`)
    - `just gen-python` (generates only the Python data models)
    - `just gen-doc` (generates schema documentation in Markdown)
    - `just site` (generates project artifacts and schema documentation)
  - **Run tests:**
    - `just test` (runs schema validation, pytest test suite, and example checks)
  - **Linter:**
    - `just lint` (runs LinkML linter on `src/ms_dcat_ap/schema/`)
  - **View docs locally:**
    - `just testdoc` (generates docs and starts local MkDocs server)
  - **Deployment:**
    - `just deploy` (publishes documentation to GitHub Pages)
  - **Install dependencies:**
    - `just install` (syncs dev dependencies with `uv`)

---

## Conventions & Rules for AI Agents

- **Modularity & Single Responsibility:**
  - Keep domain concepts modular. When adding or refactoring classes and slots, organize them by topic in modular schema files rather than monolithic definitions.
- **Profile Consistency:**
  - Whenever slots or classes are introduced or updated:
    - Define baseline slots and lenient constraints in the respective topic file or `ms_dcat_ap.yaml`.
    - Apply strict Level 1 constraints (`required: true`) in `ms_dcat_ap_level1.yaml` under `slot_usage` where MIChI compliance requires it.
- **Single Source of Truth:**
  - Only edit schema YAML files in `src/ms_dcat_ap/schema/`. Never manually edit files in `src/ms_dcat_ap/datamodel/` or `project/`.
  - Always run `just gen-project` (or `just site`) and `just test` after schema modifications.
- **Ontology & Vocabulary Referencing:**
  - All data classes should be derived from `chemdcatap`: `https://w3id.org/nfdi-de/dcat-ap-plus/chemistry/` whenever possible.
  - When defining slots, always prefer referencing terms from ontologies hosted at `https://terminology.nfdi4chem.de/ts/` (e.g., `MS:`, `CHMO:`, `OBI:`, `CHEBI:`) if a suitable term exists.
- **Example Data & Tests:**
  - Test data is located in `tests/data/` (valid/invalid examples).
  - Python unit tests in `tests/` should test both lenient and strict Level 1 models where appropriate.
