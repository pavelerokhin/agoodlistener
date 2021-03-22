INSERT INTO authors (
    author_id,
    created_at,
    favourites_count,
    followers_count,
    friends_count,
    location,
    name,
    screen_name,
    statuses_count,
    url
)
VALUES (
    {author_id},
    {created_at},
    {favourites_count},
    {followers_count},
    {friends_count},
    '{location}',
    '{name}',
    '{screen_name}',
    {statuses_count},
    '{url}'
)
