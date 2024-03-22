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

## Configuration: Dropbox API
To obtain a Dropbox API key and secret, you can folow the instructions provided by the [Dropbox tutorial](https://www.dropbox.com/developers/documentation/python#tutorial).

Dropbox no recommends creating a long-lived token with no expiration. Instead, they suggest creating a short-lived token with a refresh token which requires the key and secret obtained in the previous step. I found the following [Stack Overflow post](https://stackoverflow.com/questions/70641660/how-do-you-get-and-use-a-refresh-token-for-the-dropbox-api-python-3-x) helpful in obtaining a refresh token. The official documentation for our use case is available [here](https://dropbox-sdk-python.readthedocs.io/en/latest/api/oauth.html#dropbox.oauth.DropboxOAuth2FlowNoRedirect).

Once the Dropbox API is obtained, it can be saved as the environment variables `DROPBOX_KEY`, `DROPBOX_SECRET`, and `DROPBOX_OAUTH2_REFRESH_TOKEN` in the `.env` file.

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