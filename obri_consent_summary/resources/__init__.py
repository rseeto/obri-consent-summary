import io
import requests
import pandas as pd
from dagster import ConfigurableResource
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

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
    
class GoogleResource(ConfigurableResource):
    def get_credentials(self):
        """
        https://developers.google.com/drive/api/quickstart/python#configure_the_sample
        """
        SCOPES = 'https://www.googleapis.com/auth/drive.file'
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    def upload_file(self, file_from, file_to):
        """
        """
        SCOPES = 'https://www.googleapis.com/auth/drive.file'
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        try:
            # create drive api client
            service = build("drive", "v3", credentials=creds)

            file_metadata = {"name": file_to}
            media = MediaFileUpload(file_from, mimetype="text/csv")
            service.files().create(
                body=file_metadata, media_body=media, fields="id"
            ).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")