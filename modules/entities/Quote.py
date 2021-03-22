from modules.entities.Tweet import Tweet


class Quote(Tweet):
    def __init__(self, status):
        Tweet.__init__(self, status.quoted_status)
        self.quote_id = status.quoted_status.id
        self.tweet_id = status.id

    def get_sql_data(self):
        return {
            "quote_id": self.quote_id,
            "tweet_id": self.tweet_id,
            "author_id": self.author_id,
            "created_at": self.created_at,
            "in_reply_to_screen_name": self.in_reply_to_screen_name * 1,
            "in_reply_to_user_id": self.in_reply_to_user_id * 1,
            "has_quote": self.has_quote * 1,
            "quote_count": self.quote_count,
            "reply_count": self.reply_count,
            "retweet_count": self.retweet_count
        }
