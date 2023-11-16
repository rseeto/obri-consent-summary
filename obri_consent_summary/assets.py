import numpy as np
import pandas as pd

def summarize_enrolment(start_date, end_date, redcap_df):
    summary_dict = {}

    redcap_df = redcap_df.replace("Consent not completed", np.NaN)
    redcap_date = redcap_df.loc[
        (pd.to_datetime(redcap_df['summary_consent_date']) >= str(start_date)) 
        & (pd.to_datetime(redcap_df['summary_consent_date']) < str(end_date))
    ]
    
    summary_dict['period'] = str(start_date) + ' - ' + str(end_date)
    summary_dict['consent'] = sum(redcap_date['consent_obtained'] == 1)
    
    for rider_type in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        summary_dict['rider ' + rider_type] = sum(
            redcap_date['summary_event_' + rider_type] == 1
        )

    return summary_dict