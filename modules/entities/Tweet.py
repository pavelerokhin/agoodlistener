from modules import utils
from modules.nlp.nlp import sanitize_with_exceptions, sanitize_single_quote_for_sql, \
    extract_twitter_links, extract_text_entities


class Tweet:
    class Entity:
        def __init__(self, tweet_full_text: str, **kwargs):
            self.hashtags = kwargs.get("hashtags")
            self.urls = kwargs.get("urls")
            self.user_mentions = kwargs.get("user_mentions")
            self.symbols = kwargs.get("symbols")
            self.twitter_links = extract_twitter_links(tweet_full_text)

    def __init__(self, status):
        self.tweet_id = status.id
        self.author_id = status.author.id
        self.created_at = status.created_at.strftime("%Y%m%d%H%M%S")
        self.in_reply_to_screen_name = hasattr(status, "in_reply_to_screen_name")
        self.in_reply_to_user_id = hasattr(status, "in_reply_to_user_id")
        self.has_quote = hasattr(status, "is_quoted_status")
        self.quote_count = hasattr(status, "quote_count")
        self.reply_count = hasattr(status, "reply_count")
        self.retweet_count = hasattr(status, "retweet_count")

        self.tweet_entities_ids = []
        self.tweet_text_entities_ids = []

        self.is_extended = hasattr(status, "extended_tweet")
        self.tweet_full_text = utils.get_full_text(status, self.is_extended)
        self.entities = self.Entity(self.tweet_full_text, **status.entities)

        self.tweet_text = sanitize_with_exceptions(self.tweet_full_text, self._get_exceptions())
        self.tweet_sql_text = sanitize_single_quote_for_sql(self.tweet_text)

        self.tweet_text_entities = extract_text_entities(self.tweet_text)

    def get_sql_data_tweet(self):
        return {
            "tweet_id": self.tweet_id,
            "author_id": self.author_id,
            "created_at": self.created_at,
            "in_reply_to_screen_name": self.in_reply_to_screen_name * 1,
            "in_reply_to_user_id": self.in_reply_to_user_id * 1,
            "has_quote": self.has_quote * 1,
            "quote_count": self.quote_count,
            "reply_count": self.reply_count,
            "retweet_count": self.retweet_count,
            "tweet_text": self.tweet_sql_text
        }

    def get_sql_data_entities(self):
        return [{
            "tweet_id": self.tweet_id,
            "entity_value": "#" + sanitize_single_quote_for_sql(ht.get("text")),
            "entity_type": "hashtag",
        } for ht in self.entities.hashtags] + \
               [{
                   "tweet_id": self.tweet_id,
                   "entity_value": sanitize_single_quote_for_sql(u.get("display_url")),
                   "entity_type": "url",
               } for u in self.entities.urls] + \
               [{
                   "tweet_id": self.tweet_id,
                   "entity_value": "@" + sanitize_single_quote_for_sql(um.get("screen_name")),
                   "entity_type": "url",
               } for um in self.entities.user_mentions] + \
               [{
                   "tweet_id": self.tweet_id,
                   "entity_value": "$" + sanitize_single_quote_for_sql(s.get("text")),
                   "entity_type": "url",
               } for s in self.entities.symbols] + \
               [{
                   "tweet_id": self.tweet_id,
                   "entity_value": sanitize_single_quote_for_sql(tl),
                   "entity_type": "url",
               } for tl in self.entities.twitter_links]

    def get_sql_data_text_entities(self):
        return self.tweet_text_entities

    def _get_exceptions(self):
        hashtags = ["#" + ht.get("text") for ht in self.entities.hashtags]
        urls = [u.get("display_url") for u in self.entities.urls]
        user_mentions = ["@" + um.get("screen_name") for um in self.entities.user_mentions]
        symbols = ["$" + s.get("text") for s in self.entities.symbols]
        return hashtags + urls + user_mentions + symbols + self.entities.twitter_links

    def __str__(self):
        return f"{self.tweet_id}: " \
               f"{self.tweet_text if len(self.tweet_text) < 100 else self.tweet_text[:100] + '...'}"
