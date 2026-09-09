from pathlib import Path
from .ms_dcat_ap import *

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "ms_dcat_ap.yaml"
LEVEL1_SCHEMA_PATH = SCHEMA_DIRECTORY / "ms_dcat_ap_level1.yaml"
