import datetime
import numpy as np
import pandas as pd
from dagster import asset, op
from .resources import RedcapResource, GoogleResource

@op
def summarize_enrolment_date(start_date, end_date, redcap_df):
    """Summarize enrolment based on given dates

    Parameters
    ----------
    start_date : datetime.date
        Start date of period of interest (inclusive)
    end_date : datetime.date
        End date of period of interest (exclusive)
    redcap_df : pandas.DataFrame
        Consent data from REDCap

    Returns
    -------
    dict
        Dictionary contains the keys:
            period: time period of interest
            consent: total number of people who consented
            rider x: total number of people who consented to a specific rider
    """
    summary_dict = {}

    redcap_df = redcap_df.replace("Consent not completed", np.NaN)
    redcap_date = redcap_df.loc[
        (pd.to_datetime(redcap_df['summary_consent_date']) >= str(start_date))
        & (pd.to_datetime(redcap_df['summary_consent_date']) < str(end_date))
    ]

    summary_dict['period'] = str(start_date) + ' - ' + str(end_date-datetime.timedelta(days=1))
    summary_dict['consent'] = sum(redcap_date['consent_obtained'] == 1)

    for rider_type in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        summary_dict['rider ' + rider_type] = sum(
            redcap_date['summary_event_' + rider_type] == 1
        )

    return summary_dict

@op
def summarize_enrolment_total(start_date, end_date, delta, redcap_df):
    """Summarize enrolment based on given dates with delta resolution

    Unlike summarize_enrolment_date, this function will group enrolment into delta periods. 
    For example, if delta is set to 7, each row will represent the enrolment within a week.

    Parameters
    ----------
    start_date : datetime.date
        Start date of period of interest (inclusive)
    end_date : datetime.date
        End date of period of interest (exclusive)
    delta : datetime.timedelta
        Number of days represented in a DataFrame row
    redcap_df : pandas.DataFrame
        Consent data from REDCap

    Returns
    -------
    pandas.DataFrame
        Contains the period, consent, and all rider info over the period of interest,
        with a delta resolution. The last row contains totals for the entire time period.
    """
    rows_list = []
    while start_date <= end_date:
        rows_list.append(
            summarize_enrolment_date(start_date, start_date+delta, redcap_df)
        )
        start_date += delta
    df = pd.DataFrame(rows_list)

    # create row of totals
    df.loc[len(df.index)] = df.sum(numeric_only=True)
    df = df.astype({col: int for col in df.columns[1:]})
    df.iloc[len(df.index)-1, 0] = 'Total'

    return df

@asset
def summarize_enrolment(redcap_api: RedcapResource):
    """Create summary report and save locally

    Parameters
    ----------
    redcap_api : RedcapResource
        Dagster configurable resource to interact with REDCap
    """
    # initialize with the date we started consenting
    start_date = datetime.date(2023, 9, 11)
    today = datetime.date.today()
    delta = datetime.timedelta(days=7)

    summary = summarize_enrolment_total(
        start_date, today, delta, redcap_api.export_records()
    )

    summary.to_csv('data/OBRI Consent Summary.csv', index=False)

@asset(deps=[summarize_enrolment])
def upload_summary(gcp_api: GoogleResource):
    """Upload the local report to cloud based storage

    Parameters
    ----------
    gcp_api : GoogleResource
        Dagster configurable resource to interact with Google Cloud Platform
    """
    file_from = 'data/OBRI Consent Summary.csv'
    file_to = 'OBRI Consent Summary.csv'

    gcp_api.get_credentials()
    gcp_api.upload_file(file_from, file_to)
