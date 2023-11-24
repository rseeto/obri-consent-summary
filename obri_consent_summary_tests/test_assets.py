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

@pytest.mark.parametrize(
    'start_date_1, end_date_1, input_df_1, expected_dict_1', 
    param_summarize_enrolment_date
)

def test_summarize_enrolment_date(
    start_date_1, end_date_1, input_df_1, expected_dict_1
):
    """Test access.summarize_enrolment_date"""

    actual = summarize_enrolment_date(
        start_date_1, end_date_1, input_df_1
    )
    
    assert(actual == expected_dict_1)

param_summarize_enrolment_total = [
    (
        datetime.date(2023, 9, 11),
        datetime.date(2023, 9, 24),
        datetime.timedelta(days=7),
        pd.DataFrame(
            {
                'summary_consent_date': ['2023-09-11', '2023-09-11', '2023-09-18', '2023-09-18', '2023-09-18'],
                'consent_obtained': [1, 1, 1, 1, 1],
                'summary_event_a': [1, 1, 1, 1, 1],
                'summary_event_b': [1, 1, 0, 1, 1],
                'summary_event_c': [1, 0, 0, 1, 1],
                'summary_event_d': [1, 0, 0, 1, 1],
                'summary_event_e': [1, 0, 0, 1, 1],
                'summary_event_f': [1, 0, 0, 1, 1],
                'summary_event_g': [1, 0, 0, 1, 1],
                'summary_event_h': [1, 1, 0, 1, 1]
            }
        ),
        pd.DataFrame(
            {
                'period': pd.Series(['2023-09-11 - 2023-09-17', '2023-09-18 - 2023-09-24', 'Total'], dtype='object'),
                'consent': pd.Series([2, 3, 5], dtype=np.int32),
                'rider a': pd.Series([2, 3, 5], dtype=np.int32),
                'rider b': pd.Series([2, 2, 4], dtype=np.int32),
                'rider c': pd.Series([1, 2, 3], dtype=np.int32),
                'rider d': pd.Series([1, 2, 3], dtype=np.int32),
                'rider e': pd.Series([1, 2, 3], dtype=np.int32),
                'rider f': pd.Series([1, 2, 3], dtype=np.int32),
                'rider g': pd.Series([1, 2, 3], dtype=np.int32),
                'rider h': pd.Series([2, 2, 4], dtype=np.int32)
            }
        )
    )
]

@pytest.mark.parametrize(
    'start_date_2, end_date_2, delta_2, input_df_2, expected_df_2', 
    param_summarize_enrolment_total
)

def test_summarize_enrolment_total(
    start_date_2, end_date_2, delta_2, input_df_2, expected_df_2
):
    """Test access.summarize_enrolment_total"""

    actual = summarize_enrolment_total(
        start_date_2, end_date_2, delta_2, input_df_2
    )
    
    assert(actual.equals(expected_df_2))