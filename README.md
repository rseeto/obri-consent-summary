# OBRI-IBD: Consent Summary Pipeline
## Description
This is a [Dagster](https://dagster.io/) pipeline which extracts consent data from the [REDCap](https://www.project-redcap.org/), creates a summary, and uploads it to a Dropbox folder. It is assumed this project will be run on a Windows server which is reflected in the instructions.

## Technologies
Project is created with:
* Dagster
* REDCap API
* Python
* Dropbox

## Installation: Download repository
To run this program, this repository must be cloned or downloaded. The GitHub provided instructions on how to do this are available at [https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository.](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) 

## Installation: Virtual environment (optional)
It is best practice to create a virtual environment for this project. After you change your working directory to the local copy of this repository in Powershell, you can create a virtual environment in the local copy of this repository by entering the following commands:

```
py -3 -m venv .venv
.venv\scripts\activate
```

If you receive a message that says 'Activate.ps1 is not digitally signed. You cannot run this script on the current system.', it may be necessary to change the execution policy. For example:

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

```

## Installation: Dagster
Dagster can be installed using the following command:

```
pip install dagster dagster-webserver
```

## Installation: Dependencies
Install the Dagster dependencies using the following command:

```
pip install -e ".[dev]"
```

The `-e` flag indicates an [editable install](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs).

## Configuration
This pipeline accesses REDCap and Dropbox using their respective APIs. It is best practice to not hard-code credentials. Instead, it is recommended to create environment variables to supply the sensitive details. As [recommended by Dagster](https://docs.dagster.io/guides/dagster/using-environment-variables-and-secrets#local-development), this project uses an `.env` file to store sensitive information.

## Configuration: REDCap API
To obtain a REDCap API token, you can follow the instructions provided by [Arcus](https://education.arcus.chop.edu/redcap-api/).

Once the REDCap API is obtained, it can be saved as the environment variable `REDCAP_ACCESS_TOKEN` in the `.env` file (e.g. `REDCAP_ACCESS_TOKEN="ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"`).

## Configuration: Google Cloud Platform API
To obtain a Google Cloud Platform credentials, you can folow the instructions provided by the [Google Cloud Platform quickstart](https://developers.google.com/drive/api/quickstart/python).

For this project, the Google Drive API is necessary as it allows us to upload our file to Google Drive. The Google Drive [API needs to be enable](https://developers.google.com/drive/api/quickstart/python#enable_the_api). Google Cloud uses OAuth 2.0 to authenticate instead of API keys. To obtain credentials, it is necessary to [add yourself as a user to this project](https://developers.google.com/drive/api/quickstart/python#configure_the_oauth_consent_screen) and finally [authorize credentials for a desktop application](https://developers.google.com/drive/api/quickstart/python#authorize_credentials_for_a_desktop_application). Once the previous steps are completed, you should have access to a `credentials.json` file which will need to be placed at the top level of the project folder.

Please note, you will eventually need to change the [application publication status to "In Production"](https://support.google.com/cloud/answer/10311615#publishing-status&zippy=). If the "Publishing Status" is left as "Testing", authentification will be required every 7 days which will cause issues with the current scheduling configuration.

## Configuration: Scheduling
The Dagster pipeline is scheduled to execute once a week on Monday. To modify the execution schedule, revised the `cron_schedule` argument in `obri_consent_summary\__init__.py` using [cron syntax](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules#basic-schedules).

## Running Dagster Pipeline
Then, start the Dagster UI web server:

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

### Schedules and sensors
If you want to enable Dagster [Schedules](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules) or [Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors) for your jobs, the [Dagster Daemon](https://docs.dagster.io/deployment/dagster-daemon) process must be running. This is done automatically when you run `dagster dev`.

Once your Dagster Daemon is running, you can start turning on schedules and sensors for your jobs.

## License
[MIT](LICENSE.txt)