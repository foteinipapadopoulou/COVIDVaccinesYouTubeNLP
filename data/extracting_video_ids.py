import googleapiclient.discovery
import googleapiclient.errors

from data.utils import API_KEYS, format_date, get_country_codes, merge_all_csvs, save_list_to_csv


KEY_API = API_KEYS.get("API_2") # using the two API keys to avoid the quota limit
QUERY = 'COVID-19 vaccines'
MAX_RESULTS = 10000
NUM_PAGES = 200
VIDEOS_CSV_PATH = "videos_csv"
csv_name = "video_ids"
start_date = '2019-01-01'
end_date = '2023-11-16'


def add_to_list_check_duplicates(item, stored_ids_list):
    if item not in stored_ids_list:
        stored_ids_list.append(item)
    else:
        print(f"Video with ID: {item} has already been retrieved.")
    return stored_ids_list


def store_ids(total_results_list, stored_ids_list):
    for item in total_results_list:
        stored_ids_list = add_to_list_check_duplicates(item['id']['videoId'], stored_ids_list)
    return stored_ids_list


def get_youtube_video_ids_by_region_code(region_code):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=KEY_API)
    stored_ids = []
    next_page_token = None

    try:
        while True:
            request = youtube.search().list(
                part='id',
                q=QUERY,
                maxResults=MAX_RESULTS,
                relevanceLanguage='en', # retrieve only english videos
                type='video',
                pageToken=None if not stored_ids else next_page_token,
                publishedAfter=format_date(start_date),     # Limiting the start and end datetime to get more results
                publishedBefore=format_date(end_date)
            )
            response = request.execute()
            print(f"Response retrieved for region code : {region_code}")
            total_results_list = response['items']
            next_page_token = response.get('nextPageToken')

            # Storing the ids to the list
            stored_ids = store_ids(total_results_list, stored_ids)

            # No other results break the loop
            if not next_page_token:
                print(f"Last page token for region code : {region_code}")
                break
    except Exception as e:
        print(e)
        print(next_page_token)

    # Save the ids as csv
    ids_dict = {"ids": stored_ids}
    save_list_to_csv(ids_dict, f'{VIDEOS_CSV_PATH}/{csv_name}_{region_code}')


if __name__ == '__main__':
    "In order to maximize the results, different country codes are used to retrieve the videos."
    list_country_codes = get_country_codes()
    # Change the i and j index of the list country codes until you exceed the Youtube quota api limit
    i = 0
    j = 100

    # loop over all the country codes and extract the video ids related to the covid-19 vaccines query
    for region_code in list_country_codes[i:j]:
        get_youtube_video_ids_by_region_code(region_code)
    merge_all_csvs(VIDEOS_CSV_PATH, "merged_output")