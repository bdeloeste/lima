"""
    Bilateral Friends Algorithm
    Author: Bryan Deloeste
    Class for determining the location of a user
    from their bilateral friends.
"""
import tweepy

from collections import defaultdict
from difflib import SequenceMatcher
from random import shuffle
from time import sleep
from twitter_tokens import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

CITIES = ['Austin', 'Chicago', 'Denver', 'Los Angeles', 'Las Vegas', 'Miami', 'New York', 'Portland', 'Seattle',
          'San Fransisco', 'ATX', 'CHI', 'DEN', 'LA', 'LV', 'MIA', 'POR', 'SEA', 'SF']


class BilateralFriends(object):
    """
        Bilateral Friends algorithm that predicts the location of a given
        user depending on where the locations of a user's mutual friends.
        Mutual friends are determined by the intersection of friends
        (users that the user follows) and the followers.
    """

    def __init__(self, user_id, twitter_api):
        self.api = twitter_api
        self.user_id = user_id
        self.user_location = self.api.get_user(self.user_id).location
        self.bilateral_friends = None
        self.followers = []
        self.friends = []
        self.num_followers = 0
        self.num_friends = 0
        self._similarity_threshold = 0.7

    @staticmethod
    def _limit_handler(cursor):
        """
        Goes to sleep for 15 minutes to respect Twitter REST API limits.

        Args:
            cursor: A tweepy.Cursor object.

        Returns: None

        """
        while True:
            try:
                yield cursor.next()
            except tweepy.TweepError:
                print 'Sleeping for 15 minutes.'
                sleep(15 * 60)

    @staticmethod
    def _similarity_ratio(a, b):
        """
        Obtains ratio of the similarity between two strings.
        Args:
            a: String
            b: String

        Returns: Float depicting the ratio.

        """
        return SequenceMatcher(None, a, b).ratio()

    def get_location_occurrence(self):
        """
        TODO: FIX THIS Fi = {<ni, numi> | ni is a noun from location profile of user i's bilateral friends and numi is ni's occurrence number in location profile of i's bilateral friends

        Returns: The predicted city and state of the user.

        """
        if len(self.user_location) == 0:
            return 0
        cursor = tweepy.Cursor(self.api.followers_ids, id=self.user_id).pages()
        for follower in self._limit_handler(cursor=cursor):
            self.followers = follower
        print self.user_id, ' IDs: ', self.followers
        cursor = tweepy.Cursor(self.api.friends_ids, id=self.user_id).pages()
        for friend in self._limit_handler(cursor=cursor):
            self.friends = friend
        print self.user_id, ' IDs: ', self.friends
        self.num_followers, self.num_friends = len(self.followers), len(self.friends)
        print 'Follower count: ', str(self.num_followers)
        print 'Friends count: ', str(self.num_friends)
        set_a, set_b = set(self.followers), set(self.friends)
        self.bilateral_friends = list(set_a.intersection(set_b))
        friends_length = len(self.bilateral_friends)
        print 'Bilateral friends: ', shuffle(self.bilateral_friends)
        print 'Length: ', friends_length
        count, results_count = 0, 0
        results = defaultdict(int)
        for user_id in self.bilateral_friends:
            if count == 60:
                break
            user = self.api.get_user(user_id)
            location = user.location.lower()
            if len(location) > 0:
                results[location] += 1
                # sim = self._similarity_ratio(location, self.user_location)
                # if sim > self._similarity_threshold:
                #     results_count += 1
            count += 1
        return results


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    bilateral_friends = BilateralFriends(user_id='434673129', twitter_api=api)
    print bilateral_friends.get_location_occurrence()
    print api.rate_limit_status()['resources']['users']
