from datetime import datetime
import pandas as pd
import pycountry
import glob
import fasttext

# Run in the command line to download the model : wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
model = fasttext.load_model('lid.176.bin')

# store API keys for Youtube API
API_KEYS = {
    "API": 'AIzaSyA0WuND0jVGxdN_qCmNjl7Q0kKYuvUdmoM',
    "API_2": 'AIzaSyDqULbUnkdEJ6mrwtIE0HvNZ9MsKHXKzfs'
}


def get_country_codes():
    # Get a list of countries and their codes
    countries = list(pycountry.countries)

    # Extract country codes
    country_codes = [country.alpha_2 for country in countries]

    return country_codes


def save_list_to_csv(dict_to_be_stored, csv_name):
    df = pd.DataFrame(dict_to_be_stored)

    # Saving ids to csv
    df.to_csv(f'{csv_name}.csv', index=False)


def merge_all_csvs(folder_path, new_csv_name):

    csv_files = glob.glob(f"{folder_path}/*.csv")

    full_df = pd.DataFrame()

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        full_df = pd.concat([full_df, df])

    full_df = full_df.reset_index(drop=True)
    unique_df = full_df.drop_duplicates(keep='last')

    unique_df.to_csv(f"{new_csv_name}.csv", index=False)


def load_csv(csv_name):
    df = pd.read_csv(csv_name)
    return df


def is_english(text):
    text = str(text)
    text = text.replace('\n', ' ').strip()

    # Get the predicted language for the given text
    prediction = model.predict(text)
    # Check if the predicted language is English
    return prediction[0][0] == '__label__en'


def format_date(date_to_format):
    return datetime.strptime(date_to_format, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
