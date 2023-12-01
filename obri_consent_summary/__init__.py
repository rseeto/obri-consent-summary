from dagster import (
    Definitions, 
    load_assets_from_modules,
    EnvVar,
    AssetSelection,
    define_asset_job,
    ScheduleDefinition
)
from . import assets
from .resources import RedcapResource

all_assets = load_assets_from_modules([assets])

obri_consent_summary_job = define_asset_job("obri_consent_summary_job", selection=AssetSelection.all())

obri_consent_summary_schedule = ScheduleDefinition(
    job=obri_consent_summary_job,
    cron_schedule="0 07 * * MON"
)

defs = Definitions(
    assets=all_assets,
    resources={
        "redcap_api": RedcapResource(redcap_access_token=EnvVar("REDCAP_ACCESS_TOKEN"))
    },
    schedules=[obri_consent_summary_schedule]
)
