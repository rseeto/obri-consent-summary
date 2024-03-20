import io
import requests
import pandas as pd
from dagster import ConfigurableResource
import dropbox


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

class DropboxResource(ConfigurableResource):
    dropbox_key: str
    dropbox_secret: str
    dropbox_oauth2_refresh_token: str

    def upload_file(self, file_from, file_to):

        dbx = dropbox.Dropbox(
            app_key=self.dropbox_key,
            app_secret=self.dropbox_secret,
            oauth2_refresh_token=self.dropbox_oauth2_refresh_token
        )

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to,  mode=dropbox.files.WriteMode.overwrite)