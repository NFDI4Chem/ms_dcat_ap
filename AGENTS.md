# AGENTS.md

## Overview

This project implements a domain-specific DCAT-AP profile for mass spectrometry (MS) according to MIChI recommendations. The central data structure is a LinkML schema (`src/ms_dcat_ap/schema/ms_dcat_ap.yaml`), from which various artifacts (e.g., Python data model, documentation, validation rules) are generated.

---

## Architecture & Main Components

- **Schema Definition:**
  - `src/ms_dcat_ap/schema/ms_dcat_ap.yaml` is the authoritative source for all model and validation rules.
  - Changes to the schema require regeneration of artifacts (see workflows).
- **Generated Artifacts:**
  - `src/ms_dcat_ap/datamodel/`: Contains the generated Python data model (e.g., `ms_dcat_ap.py`, `ms_dcat_ap_pydantic.py`).
  - `project/`: Contains further generated artifacts (e.g., Java, TypeScript, OWL, JSON-Schema). Never edit, always regenerate!
- **Documentation:**
  - `docs/` contains the MkDocs-generated documentation. Schema documentation is generated into `docs/elements/`.
- **Example Data & Tests:**
  - Example data is in `tests/data/` (valid/invalid). Examples are generated into `examples/output/`.
  - Tests are in `tests/`.

---

## Developer Workflows

- **Command Overview:**
  - Use the [`just`](https://github.com/casey/just) tool for all build, test, and generation tasks.
  - `just` or `just --list` shows all available commands.
- **Typical Workflows:**
  - **Generate artifacts:**
    - `just gen-project` (generates all artifacts including Python model)
    - `just gen-doc` (generates schema documentation)
    - `just site` (generates everything for the docs)
  - **Run tests:**
    - `just test` (runs schema, Python, and example tests)
  - **Linter:**
    - `just lint` (runs LinkML lint on the schema)
  - **View docs locally:**
    - `just testdoc` (starts local MkDocs server)
  - **Deployment:**
    - `just deploy` (publishes docs to GitHub Pages)
  - **Install dependencies:**
    - `just install` (uses `uv` for dependency management)

---

## Conventions & Special Notes

- **Schema as Single Source of Truth:**
  - Only edit `src/ms_dcat_ap/schema/ms_dcat_ap.yaml`, never generated files.
- **Never manually change files in `project/`.**
- **Example and test data:**
  - Example and test data is processed from `tests/data/`.
- **Dependencies:**
  - Python >=3.9, dependency management via `uv` (see `pyproject.toml`).
  - Dev dependencies in `[dependency-groups]` in `pyproject.toml`.
- **Docs and artifact generation:**
  - Many artifacts are generated from the schema (see `justfile`).
- **Upstream template:**
  - The project is based on [linkml-project-copier](https://github.com/dalito/linkml-project-copier). Template updates via `just update`.

---

## Examples & References

- **Schema:** `src/ms_dcat_ap/schema/ms_dcat_ap.yaml`
- **Python model:** `src/ms_dcat_ap/datamodel/ms_dcat_ap.py`
- **Tests:** `tests/`, `tests/data/`
- **Examples:** `examples/`
- **Docs:** `docs/`, `docs/elements/`
- **justfile:** Central definition of all workflows
- **pyproject.toml:** Dependency and build management

---

## Guidance for AI Agents

- Always use the schema as the starting point for model changes.
- Never manually edit generated files.
- Always use `just` for workflows.
- If unsure: See README.md and the generated docs (`docs/`).
- All data classes should be derived from `chemdcatap`: https://w3id.org/nfdi-de/dcat-ap-plus/chemistry/ whenever possible.
- When defining slots, always prefer referencing terms from ontologies hosted at https://terminology.nfdi4chem.de/ts/ if a suitable term exists.
