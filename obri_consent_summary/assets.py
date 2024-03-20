import datetime
import numpy as np
import pandas as pd
from dagster import asset, op
from .resources import RedcapResource, GoogleResource

@op
def summarize_enrolment_date(start_date, end_date, redcap_df):
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
    
    rows_list = []
    while (start_date <= end_date):
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
    # initialize with the date we started consenting
    start_date = datetime.date(2023, 9, 11)
    today = datetime.date.today()
    delta = datetime.timedelta(days=7)

    summarize_enrolment = summarize_enrolment_total(start_date, today, delta, redcap_api.export_records())

    summarize_enrolment.to_csv('data/OBRI Consent Summary.csv', index=False)

@asset(deps=[summarize_enrolment])
def upload_summary(gcp_api: GoogleResource):
    file_from = 'data/OBRI Consent Summary.csv'
    file_to = 'OBRI Consent Summary.csv'
    
    gcp_api.get_credentials()
    gcp_api.upload_file(file_from, file_to)