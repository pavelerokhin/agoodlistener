CREATE TABLE IF NOT EXISTS quotes (
    quote_id integer PRIMARY KEY,
    tweet_id integer,
    author_id integer,
    created_at integer,
    in_reply_to_screen_name tinyint,
    in_reply_to_user_id tinyint,
    has_quote tinyint,
    quote_count integer,
    reply_count integer,
    retweet_count integer
)