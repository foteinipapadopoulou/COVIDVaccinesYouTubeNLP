"""Class Comment representing the necessary fields of a comment.
More fields than necessary have been extracted from the API, in case they are needed in the future for other research."""
class Comment:
    def __init__(self, id, text, publish_date, like_count, channel_id, author_channel_id, video_id):
        self.id = id
        self.text = text
        self.publish_date = publish_date
        self.like_count = like_count
        self.video_id = video_id
        self.author_channel_id = author_channel_id
        self.channel_id = channel_id


def create_comment(top_level_comment):
    snippet = top_level_comment['snippet']
    comment_id = top_level_comment['id']
    comment_text = snippet['textDisplay']
    comment_published_date = snippet['publishedAt']
    comment_like_count = snippet['likeCount']
    comment_channel_id = snippet['channelId']
    if 'authorChannelId' in snippet and 'value' in snippet['authorChannelId']:
        comment_author_channel_id = snippet['authorChannelId']['value']
    else:
        comment_author_channel_id = ''
    comment_video_id = snippet['videoId']

    c = Comment(comment_id, comment_text, comment_published_date, comment_like_count,
                    comment_channel_id, comment_author_channel_id, comment_video_id)

    return c
