import numpy as np
import pandas as pd
import datetime

def get_redcap_record():
    pass

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

def summarize_enrolment():
    # initialize with the date we started consenting
    start_date = datetime.date(2023, 9, 11)
    today = datetime.date.today()
    delta = datetime.timedelta(days=7)

    redcap_df = get_redcap_record()

    summarize_enrolment = summarize_enrolment_total(start_date, today, delta, redcap_df)

    summarize_enrolment.to_csv('OBRI Consent Summary.csv', index=False)