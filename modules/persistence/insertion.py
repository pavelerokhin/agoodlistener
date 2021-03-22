from typing import List

from modules.persistence.dbaccess import execute_query
from modules.persistence.orchestration import QUERIES
from modules.persistence.retrieval import author_exists


def prepare_unique_query(query, values):
    return QUERIES[query].format(**values)


def prepare_multiple_query(query, list_dictionaries, *, tweet_id=None):
    populated_query = ""
    for values in list_dictionaries:
        if tweet_id:
            populated_query += prepare_unique_query(query, {**values, "tweet_id": tweet_id}) + "; "
        else:
            populated_query += prepare_unique_query(query, values) + "; "
    return populated_query


def persist_entities(conn, tweet_id, entities: List):
    populated_query = prepare_multiple_query("INSERT_ENTITY", entities, tweet_id=tweet_id)
    execute_query(conn, populated_query)


def persist_text_entities(conn, tweet_id, entities: List):
    populated_query = prepare_multiple_query("INSERT_TEXT_ENTITY", entities, tweet_id=tweet_id)
    execute_query(conn, populated_query)


def persist(conn, tweet, quote, author):
    execute_query(conn, QUERIES["INSERT_TWEET"].format(**tweet.get_sql_data_tweet()))
    if quote:
        execute_query(conn, QUERIES["INSERT_QUOTE"].format(**quote.get_sql_data()))

    if not author_exists(conn, author.author_id):
        execute_query(conn, QUERIES["INSERT_AUTHOR"].format(**author.get_sql_data()))

    persist_entities(conn, tweet.tweet_id, tweet.get_sql_data_entities())
    persist_text_entities(conn, tweet.tweet_id, tweet.get_sql_data_text_entities())
