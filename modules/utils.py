import sys
import yaml
from datetime import datetime


def open_and_parse_yaml(file_name, error_message):
    conf = ""
    try:
        with open(file_name, "r") as file:
            conf = yaml.load(file, Loader=yaml.FullLoader)
            if not conf:
                print(error_message)
                sys.exit(1)
    except FileNotFoundError:
        print("file", file_name, "does not exist")
        sys.exit(1)  # TODO: return an Error

    return conf


def get_full_text(status, is_extended):
    if is_extended:
        return status.extended_tweet["full_text"]
    status_text = status.text
    try:
        retweeted_status_text = status.retweeted_status.text
    except AttributeError:
        return status_text

    try:
        retweeted_status_extended_tweet_text = status.retweeted_status.extended_tweet.get('full_text')
    except AttributeError:
        return retweeted_status_text
    return retweeted_status_extended_tweet_text


def simple_logger(place, message):
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("{} - {}: {}".format(time, place, message))