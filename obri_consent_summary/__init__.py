from dagster import (
    Definitions, 
    load_assets_from_modules,
    EnvVar
)
from . import assets
from .resources import RedcapResource

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "redcap_api": RedcapResource(redcap_access_token=EnvVar("REDCAP_ACCESS_TOKEN"))
    }
)
