# main launcher
import getopt
import sys

from modules.persistence.errors import SQLiteConnectionError, InsufficientConfigurationError
from modules.persistence.orchestration import orchestrate_db_connection
from modules.twitterlistener import stream_go

from modules.utils import open_and_parse_yaml


if __name__ == "__main__":
    configFilePath = "conf.yml"
    twitterFilePath = "twitter_keys.yml"

    # TODO: remake it with an appropriate library
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:c:", ["twitter-keys=", "config="])
    except getopt.GetoptError:
        print("CLI command syntax error")
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            print("HELP")
            sys.exit(0)
            # TODO: add help file and text
        elif opt in ["-t", "--twitter-keys"]:
            twitterFilePath = arg
        elif opt in ["-c", "--config"]:
            configFilePath = arg
    print("config file:", configFilePath)
    print("twitter keys file:", twitterFilePath)

    # get config
    conf = open_and_parse_yaml(configFilePath, "no configuration file")
    # get twitter keys
    keys = open_and_parse_yaml(twitterFilePath, "no twitter keys file")

    conn = None
    try:
        conn = orchestrate_db_connection(conf)
        stream_go(conf, keys, conn)
    except (SQLiteConnectionError, InsufficientConfigurationError) as e:
        print(e.message)
        sys.exit(1)
    finally:
        if conn:
            conn.close()
