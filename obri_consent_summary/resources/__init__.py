import requests
import pandas as pd
import io
from dagster import ConfigurableResource


class RedcapResource(ConfigurableResource):
    redcap_access_token: str

    def export_records(self):
        data = {
            'token': self.redcap_access_token,
            'content': 'record',
            'action': 'export',
            'format': 'csv',
            'type': 'flat',
            'csvDelimiter': '',
            'rawOrLabel': 'raw',
            'rawOrLabelHeaders': 'raw',
            'exportCheckboxLabel': 'false',
            'exportSurveyFields': 'false',
            'exportDataAccessGroups': 'false',
            'returnFormat': 'json'
        }
        req = requests.post('http://ddcrc03/redcap/api/', data=data).content
        redcap_df = pd.read_csv(
            io.StringIO(req.decode('utf-8')),
            sep = ","
        )

        return redcap_df