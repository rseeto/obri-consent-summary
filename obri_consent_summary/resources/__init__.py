import io
import os.path
import requests
import pandas as pd
from dagster import ConfigurableResource, get_dagster_logger
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

class RedcapResource(ConfigurableResource):
    """Custom Dagster resource to interact with REDCap

    Parameters
    ----------
    ConfigurableResource : dagster.ConfigurableResource
        Parameter is necessary to interact with Dagster.

    Notes
    -----
        See https://docs.dagster.io/concepts/resources for more info.
    """
    redcap_access_token: str

    def export_records(self):
        """Export records from REDCap API

        Returns
        -------
        pandas.DataFrame
            Returns a all exported records from REDCap in a DataFrame.
        """
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
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
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
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        file_id = self._get_file_id(creds)

        get_dagster_logger().info(file_id)

        try:
            # create drive api client
            service = build("drive", "v3", credentials=creds)
            media = MediaFileUpload(file_from, mimetype="text/csv")

            # If not file has previously been loaded, log link to access file
            if file_id is None:
                file_metadata = {"name": file_to}
                file = service.files().create(
                    body=file_metadata, media_body=media, fields="id"
                ).execute()

                self._get_share_link(service, file.get("id"))
            else:
                service.files().update(fileId=file_id, media_body=media).execute()
        except HttpError as error:
            get_dagster_logger().info(f"An error occurred: {error}")

    def _get_share_link(self, service, file_id):
        """
        """
        request_body = {
            'role': 'reader',
            'type': 'anyone'
        }

        service.permissions().create(
            fileId=file_id, body=request_body
        ).execute()
        response_share_link = service.files().get(fileId=file_id, fields='webViewLink').execute()

        get_dagster_logger().info(response_share_link['webViewLink'])

    def _get_file_id(self, creds):
        """
        """
        try:
            # create drive api client
            service = build("drive", "v3", credentials=creds)

            # Call the Drive v3 API
            results = (
                service.files()
                .list(pageSize=10, fields="nextPageToken, files(id, name)")
                .execute()
            )
            items = results.get("files", [])

            if not items:
                file_id = None
            else:
                file_id = items[0]['id']

            return file_id

        except HttpError as error:
            get_dagster_logger().info(f"An error occurred: {error}")
