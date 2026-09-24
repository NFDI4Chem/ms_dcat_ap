# Example data for ms_dcat_ap and ms_dcat_ap_level1

This folder contains example data for testing and demonstrating the datamodels,
separated by profile:

## Profile Structures

### 1. `legacy/` (Base Profile `ms_dcat_ap.yaml`)
- `legacy/valid/`: Example data conforming to the base/legacy profile (e.g., MSBNK-IPB_Halle-PB001341 modular examples).
- `legacy/invalid/`: Counter-examples violating base profile schema rules.

### 2. `level1/` (Strict Profile `ms_dcat_ap_level1.yaml`)
- `level1/valid/`: Example data strictly conforming to MIChI Level 1 requirements.
- `level1/invalid/`: Counter-examples violating strict Level 1 rules (e.g. missing required experimental/instrument metadata).

## Filename Conventions
The filenames of all example data must conform to the scheme `ClassName-###.yaml`
where `ClassName` must be the name of a class from the schema. "###" can be a number
or one or more other characters allowed in filenames. The class name is derived by
splitting at the first "-" and taking the part before the "-".
