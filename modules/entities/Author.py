from modules.nlp.nlp import sanitize_single_quote_for_sql


class Author:
    def __init__(self, status):
        self.author_id = status.author.id
        self.created_at = status.author.created_at.strftime("%Y%m%d%H%M%S")
        self.favourites_count = status.author.favourites_count
        self.followers_count = status.author.followers_count
        self.friends_count = status.author.friends_count
        self.location = status.author.location
        self.name = status.author.name
        self.screen_name = status.author.screen_name
        self.statuses_count = status.author.statuses_count
        self.url = status.author.url

    def get_sql_data(self):
        return {
            "author_id": self.author_id,
            "created_at": self.created_at,
            "favourites_count": self.favourites_count,
            "followers_count": self.followers_count,
            "friends_count": self.friends_count,
            "location": sanitize_single_quote_for_sql(self.location),
            "name": sanitize_single_quote_for_sql(self.name),
            "screen_name": sanitize_single_quote_for_sql(self.screen_name),
            "statuses_count": self.statuses_count,
            "url": sanitize_single_quote_for_sql(self.url)
        }
