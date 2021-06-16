CREATE TABLE IF NOT EXISTS authors (
    author_id integer PRIMARY KEY,
    created_at integer,
    favourites_count integer,
    followers_count integer,
    friends_count integer,
    location text,
    name text,
    screen_name text,
    statuses_count integer,
    url text
)
