import pandas as pd

from data.utils import  load_csv, is_english
from extracting_comments import COMMENTS_CSV_PATH

FILTERED_DATETIME_COMMENTS_CSV_NAME = "filtered_datetime_comments"
FILTERED_ENGLISH_COMMENTS_CSV_NAME = "filtered_english_comments"


def filter_datetime(df_comments, start_date, end_date):
    header_date_name = "publish_date"

    df_comments[header_date_name] = pd.to_datetime(df_comments[header_date_name], format='%Y-%m-%dT%H:%M:%SZ')
    df_filtered = df_comments.loc[(df_comments[header_date_name] >= start_date)
                     & (df_comments[header_date_name] < end_date)]

    return df_filtered


def filter_english(df_comments):

    df_comments['is_english'] = df_comments["text"].apply(is_english)

    df_filtered = df_comments[df_comments['is_english']]
    # discard the non-English comment
    df_filtered = df_filtered.drop(columns=['is_english'])
    return df_filtered

"""
Filtering the dataset remove the duplicate rows
then getting the rows with publish date from 11/08/2021 - 13/12/2023
and then keeping only the english comments
"""
if __name__ == '__main__':
    file_name = ''
    df_comments = load_csv(f'{COMMENTS_CSV_PATH}/{file_name}.csv')
    start_date_str = "2020-08-11T00:00:00Z"
    end_date_str = "2023-12-13T00:00:00Z"
    start_date = pd.to_datetime(start_date_str, format='%Y-%m-%dT%H:%M:%SZ')
    end_date = pd.to_datetime(end_date_str, format='%Y-%m-%dT%H:%M:%SZ')

    df_comments_datetime_filtered = filter_datetime(df_comments, start_date, end_date)
    df_comments_datetime_filtered.to_csv(f"{COMMENTS_CSV_PATH}/{FILTERED_DATETIME_COMMENTS_CSV_NAME}.csv", index=False)

    df_comments_english_filtered = filter_english(df_comments_datetime_filtered)
    df_comments_english_filtered.to_csv(f"{COMMENTS_CSV_PATH}/{FILTERED_ENGLISH_COMMENTS_CSV_NAME}.csv", index=False)