import traceback

import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

from data.Comment import create_comment
from data.utils import API_KEYS, load_csv
from data.extracting_video_ids import VIDEOS_CSV_PATH

KEY_API = API_KEYS.get("API_2") # using the two API keys to avoid the quota limit
VIDEO_IDS_CSV_NAME = f'{VIDEOS_CSV_PATH}/merged_output.csv'
COMMENTS_CSV_PATH = "comments_csv"


def get_youtube_comments_by_video_id(video_id, comments_list, disabled_comments_videos, no_comments_videos):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=KEY_API)

    next_page_token = None
    while True:
        # define the parameters request
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            pageToken=next_page_token,
            maxResults=100,
            textFormat='plainText'
        )
        try:
            # send the request
            response = request.execute()
        except Exception as e:
            if hasattr(e, 'error_details') and e.error_details[0]["reason"] == "commentsDisabled":
                print(f"Video ID :{video_id} has disabled comments")
                disabled_comments_videos.append(video_id)
                break
            elif hasattr(e, 'error_details') and e.error_details[0]["reason"] == "videoNotFound":
                print(f"Video ID :{video_id} not found")
                break
            else:
                raise e
        next_page_token = response.get('nextPageToken')

        # get the comments and store to the list
        for item in response['items']:
            comment = create_comment(item['snippet']['topLevelComment'])
            comments_list.append(comment)

        if not response['items']:
            print(f"Video ID :{video_id} doesn't have comments")
            no_comments_videos.append(video_id)

        # No other results found break the loop
        if not next_page_token:
            print(f"Last page token for video id : {video_id}")
            break

    comments_df = pd.DataFrame([
        {'id': comment.id,
         'text': comment.text,
         'publish_date': comment.publish_date,
         'like_count': comment.like_count,
         'video_id': comment.video_id,
         'author_channel_id': comment.author_channel_id,
         'channel_id': comment.channel_id}
        for comment in comments_list
    ])
    comments_df.to_csv(f"{COMMENTS_CSV_PATH}/output.csv", mode='a' ,index=False, header=False)
    return disabled_comments_videos, no_comments_videos

def get_youtube_comments(video_ids_csv_name):
    comments = []
    disabled_comments_videos = []
    no_comments_videos = []
    video_ids = load_csv(video_ids_csv_name)["ids"]
    try:
        for id in video_ids:
            get_youtube_comments_by_video_id(id, comments, disabled_comments_videos, no_comments_videos)
    except Exception as e:
        print(traceback.format_exc())
        print(e)

    # save the videos with no comments and the videos with disabled comments to csv
    df_disabled_comments = pd.DataFrame(disabled_comments_videos)
    df_no_comments = pd.DataFrame(no_comments_videos)

    df_no_comments.to_csv(f"{COMMENTS_CSV_PATH}/no_comments_video_ids.csv",  index=False, header=False)
    df_disabled_comments.to_csv(f"{COMMENTS_CSV_PATH}/disabled_comments_video_ids.csv",  index=False, header=False)

if __name__ == '__main__':
    get_youtube_comments(VIDEO_IDS_CSV_NAME)
