import tweepy

from modules.entities.Author import Author
from modules.entities.Quote import Quote
from modules.entities.Tweet import Tweet
from modules.persistence.insertion import persist


def stream_go(conf, keys, conn):
    """
    main function launching twitter filtered streaming
    input from config file, file with Twitter credentials
    output goes to the output/[csv_file]
    """
    # authorisation
    auth = tweepy.OAuthHandler(consumer_key=keys.get('customer_key'),
                               consumer_secret=keys.get('customer_secret'))
    auth.set_access_token(key=keys.get('access_key'), secret=keys.get('access_secret'))
    api = tweepy.API(auth_handler=auth)

    # stream
    stream_listener = StreamListener(conf, conn)
    stream = tweepy.Stream(auth=api.auth,
                           listener=stream_listener,
                           tweet_mode='extended',
                           timeout=conf.get("timeout"))

    # go!
    stream.filter(languages=conf.get('language'), track=conf.get('tags'))


class StreamListener(tweepy.StreamListener):
    def __init__(self, configuration, db_connection):
        super(StreamListener, self).__init__()
        self.conf = configuration
        self.conn = db_connection
        self.messages_counter = 0
        self.max_messages = configuration.get("max_messages")

    def on_status(self, status):

        if self.max_messages and self.messages_counter >= self.max_messages:
            print(f"Max number of messages {self.max_messages} reached")
            return False

        self.messages_counter += 1

        tweet = Tweet(status)
        author = Author(status)
        quote = None
        if tweet.has_quote:
            quote = Quote(status)

        print(self.messages_counter, tweet)

        # persistence
        persist(self.conn, tweet, quote, author)

    def on_disconnect(self, notice):
        print("A Good Listener has disconnected")
        return

    def on_error(self, status_code):
        print("A Good Listener had an error in streaming", status_code)

    def on_exception(self, exception):
        print("A Good Listener had an exception in streaming", exception)
        return


