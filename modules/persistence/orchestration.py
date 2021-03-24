import os

from modules.persistence.dbaccess import create_db_if_needed_and_get_connection, execute_query
from modules.persistence.errors import InsufficientConfigurationError


QUERIES = {}


def orchestrate_db_connection(conf):
    db_file = conf.get('dbPath')
    if not db_file:
        raise InsufficientConfigurationError("no DB filepath available")

    if os.path.exists(db_file) and conf.get('replaceDatabase'):
        os.remove(db_file)

    # create connection and DB if not exist
    conn = create_db_if_needed_and_get_connection(db_file)

    if conf.get('replaceDatabase'):
        create_schema(conn, db_file) # correct it

    load_inner_queries()  # TODO: make it without global vars

    return conn


def create_schema(conn, db_file):
    if conn:
        schema_path = "db/dbschema/"
        schema_scripts = [schema_path + script_name for script_name in os.listdir(schema_path)]

        for ss in schema_scripts:
            with open(ss, "r") as schema_file:
                schema_script = schema_file.read().replace("\n", " ")
            execute_query(conn, schema_script)


def load_inner_queries():
    queries_path = "db/queries/"
    query_names = [queries_path + script_name for script_name in os.listdir(queries_path)
                   if len(script_name) >= 5 and script_name[-4:] == ".sql"]

    for query_name in query_names:
        with open(query_name) as q:
            key_query_name = query_name.split("/")[-1][:-4].upper()
            QUERIES[key_query_name] = q.read().replace("\n", " ")
