from obri_consent_summary.assets import *
import pandas as pd
import pytest
import datetime

param_summarize_enrolment_date = [
    (
        datetime.date(2023, 9, 11),
        datetime.date(2023, 9, 18),
        pd.DataFrame(
            {
                'summary_consent_date': ['2023-09-11', '2023-09-12', '2023-09-17', '2023-09-18'],
                'consent_obtained': [1, 0, 1, 1],
                'summary_event_a': [1, 0, 1, 1],
                'summary_event_b': [1, 0, 0, 1],
                'summary_event_c': [1, 0, 0, 1],
                'summary_event_d': [1, 0, 0, 1],
                'summary_event_e': [1, 0, 0, 1],
                'summary_event_f': [1, 0, 0, 1],
                'summary_event_g': [1, 0, 0, 1],
                'summary_event_h': [1, 0, 0, 1]
            }
        ),
        {
            'period': '2023-09-11 - 2023-09-17',
            'consent': 2,
            'rider a': 2,
            'rider b': 1,
            'rider c': 1,
            'rider d': 1,
            'rider e': 1,
            'rider f': 1,
            'rider g': 1,
            'rider h': 1
        }
    ),
    (
        datetime.date(2023, 9, 11),
        datetime.date(2023, 9, 18),
        pd.DataFrame(
            {
                'summary_consent_date': ['2023-09-11', np.NaN, '2023-09-17', '2023-09-18'],
                'consent_obtained': [1, 0, 1, 1],
                'summary_event_a': [1, 0, 1, 1],
                'summary_event_b': [1, 0, 0, 1],
                'summary_event_c': [1, 0, 0, 1],
                'summary_event_d': [1, 0, 0, 1],
                'summary_event_e': [1, 0, 0, 1],
                'summary_event_f': [1, 0, 0, 1],
                'summary_event_g': [1, 0, 0, 1],
                'summary_event_h': [1, 0, 0, 1]
            }
        ),
        {
            'period': '2023-09-11 - 2023-09-17',
            'consent': 2,
            'rider a': 2,
            'rider b': 1,
            'rider c': 1,
            'rider d': 1,
            'rider e': 1,
            'rider f': 1,
            'rider g': 1,
            'rider h': 1
        }
    ),
    (
        datetime.date(2023, 9, 11),
        datetime.date(2023, 9, 18),
        pd.DataFrame(
            {
                'summary_consent_date': ['2023-09-11', np.NaN, '2023-09-17', '2023-09-18'],
                'consent_obtained': [1, 0, 1, 1],
                'summary_event_a': [1, 0, 1, 1],
                'summary_event_b': [1, 0, 0, 1],
                'summary_event_c': [1, 0, 0, 1],
                'summary_event_d': [1, 0, 0, 1],
                'summary_event_e': [1, 0, 0, 1],
                'summary_event_f': [1, 0, 0, 1],
                'summary_event_g': [1, 0, 0, 1],
                'summary_event_h': [1, 0, 0, 1]
            }
        ),
        {
            'period': '2023-09-11 - 2023-09-17',
            'consent': 2,
            'rider a': 2,
            'rider b': 1,
            'rider c': 1,
            'rider d': 1,
            'rider e': 1,
            'rider f': 1,
            'rider g': 1,
            'rider h': 1
        }
    )
]