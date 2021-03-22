from modules.persistence.dbaccess import execute_query
from modules.persistence.orchestration import QUERIES


def author_exists(conn, author_id):
    result = execute_query(conn, QUERIES["GET_AUTHOR_BY_ID"].format(author_id),
                           execute_script=False, is_to_commit=False)
    return result.fetchone()


def retrieve_tweet_by_id(conn, values):
    populated_query = QUERIES["RETRIEVE_TWEET_BY_ID"].format(*values)
    return execute_query(conn, populated_query)


def retrieve_tweet_by_text(conn, values):
    populated_query = QUERIES["RETRIEVE_TWEET_BY_WORDS"].format(*values)
    return execute_query(conn, populated_query)


def retrieve_quote_by_text(conn, values):
    populated_query = QUERIES["RETRIEVE_QUOTE_BY_WORDS"].format(*values)
    return execute_query(conn, populated_query)
