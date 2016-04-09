"""
    Asynchronous Twitter Stream Class
    Author: Bryan Deloeste
    Process that streams all tweets from continental America,
    infers location, provides lima score, and stores them in the 'stream_buffer' collection

    Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
    Sentiment Analysis of Social Media Text. Eighth International Conference on
    Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
"""

import sys

from json import loads
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pymongo import MongoClient, DESCENDING, TEXT
from threading import Thread, ThreadError
from time import sleep, time
from tweepy import API, StreamListener, streaming, OAuthHandler
from twitter_tokens import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


AUTH = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

CLIENT = MongoClient('localhost', 27017)
TRAINING_SET_DB = CLIENT['test']
STREAM_BUFFER = TRAINING_SET_DB['stream_buffer']

CONTINENTAL_AMERICA = [-125.0011, 24.9493, -66.9326, 49.5904]


class ApplicationStream(StreamListener):
    """
        Stream handler class that receives incoming tweets and
        determines location (if None), scores the sentiment
        of the tweet and stores incoming tweet to 'stream_buffer'
        collection.
    """
    def __init__(self, twitter_api):
        super(StreamListener, self).__init__()
        self.api = twitter_api

    def on_data(self, raw_data):
        tweet = loads(raw_data)
        try:
            text = tweet['text']
            if tweet.get('retweeted_status') is None and 'RT @' not in text:
                if 'coordinates' not in tweet:
                    print 'needs location inference'
                sentiment_analyzer = SentimentIntensityAnalyzer()
                sentiment_score = sentiment_analyzer.polarity_scores(text=text)['compound']
                tweet['sentiment'] = sentiment_score
                current_time_ms = int(round(time() * 1000))
                tweet['time_inserted'] = current_time_ms
                print text, ': ', str(sentiment_score)
                STREAM_BUFFER.insert(tweet)
        except KeyError, v:
            print 'KeyError: ', v


def reindex_thread():
    """
    Periodically reindexes 'stream_buffer' collection every 5 minutes.
    {
        'text': pymongo.TEXT,
        'timestamp_ms': pymongo.DESCENDING
    }
    """
    while True:
        indexes = STREAM_BUFFER.index_information()
        if len(indexes) == 1:
            print 'Creating \'text\' and \'timestamp_ms\' indexes..'
            STREAM_BUFFER.create_index(
                [('text', TEXT), ('time_inserted', DESCENDING)],
                background=True)
        else:
            print 'Reindexing'
            STREAM_BUFFER.reindex()
        print 'Reindexing thread going to sleep.'
        sleep(60)


if __name__ == '__main__':
    keywords = None
    try:
        keywords = sys.argv[1:]
    except TypeError:
        print >> sys.stderr, "Caught TypeError"
    api = API(AUTH)
    stream = streaming.Stream(AUTH, ApplicationStream(api))

    if STREAM_BUFFER.count() > 0:
        try:
            print 'Starting reindexing thread...'
            thread = Thread(target=reindex_thread)
            thread.daemon = True
            thread.start()
        except ThreadError:
            print 'Sorry, something went wrong with the reindexing thread'

    while True:
        print 'Starting new stream'
        if keywords is not None:
            stream.filter(languages=['en'], locations=CONTINENTAL_AMERICA)
