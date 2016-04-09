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
        self.user_id = user_id
        self.api = twitter_api
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

    def get_bilateral_friends(self):
        """
        Checks for

        Returns: The predicted city and state of the user.

        """
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
        possible_results = defaultdict(int)
        count, results_count = 0, 0
        for user_id in self.bilateral_friends:
            if count == 60:
                friends_length = count
                break
            user = self.api.get_user(user_id)
            location = user.location
            if len(location) == 0:
                continue
            else:
                print str(len(location)), location
                count += 1
                for city in CITIES:
                    sim = self._similarity_ratio(location, city)
                    if sim > self._similarity_threshold:
                        if city == 'Austin' or city == 'ATX':
                            possible_results['Austin'] += 1
                        elif city == 'Chicago' or city == 'CHI':
                            possible_results['Chicago'] += 1
                        elif city == 'Denver' or city == 'DEN':
                            possible_results['Denver'] += 1
                        elif city == 'Los Angeles' or city == 'LA':
                            possible_results['Austin'] += 1
                        elif city == 'Las Vegas' or city == 'LV':
                            possible_results['Las Vegas'] += 1
                        elif city == 'Miami' or city == 'MIA':
                            possible_results['Miami'] += 1
                        elif city == 'New York' or city == 'NY':
                            possible_results['New York'] += 1
                        elif city == 'Portland' or city == 'POR':
                            possible_results['Portland'] += 1
                        elif city == 'Seattle' or city == 'SEA':
                            possible_results['Seattle'] += 1
                        elif city == 'San Fransisco' or city == 'SF':
                            possible_results['San Fransisco'] += 1
                        results_count += 1
        print possible_results
        guess_threshold = friends_length / 10
        result = max(possible_results.iteritems(), key=lambda x: x[1])
        if result[1] > guess_threshold:
            print 'I predict that', self.user_id, 'is from', result[0]
            return result[1]
        print 'Could not guess where user', self.user_id, 'is from'
        return 'None'


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    bilateral_friends = BilateralFriends(user_id='434673129', twitter_api=api)
    bilateral_friends.get_bilateral_friends()
    print api.rate_limit_status()['resources']['users']
