"""
Location Inference Model
Author: Bryan Deloeste

Source: http://www.jcomputers.us/vol9/jcp0902-09.pdf
"""
from collections import defaultdict
from math import log


class LocationInference(object):
    def __init__(self, user, local_words, geo_words):
        """
        ci = <ui, gi, Fi, Ti>
        Args:
            user:  { 'id': tweet['user']['id'],
                     'location': tweet['user']['location'],
                     'bilateral_friends_location_occurrences': loc_occurrence_count,
                     'text_nouns': tweet_nouns }
        """
        self._delta = 10.0
        self._lambda = 1.0
        self.user = user
        self.gazetteer_words = {'Austin', 'Chicago', 'Denver', 'Los Angeles', 'Las Vegas', 'Miami', 'New York',
                                'Portland', 'Seattle', 'San Fransisco'}
        self.local_words = local_words
        self.geo_words = geo_words

    def get_location(self):
        """

        Returns:

        """
        g_weights = defaultdict(int)
        for g in self.gazetteer_words:
            for geo in self.geo_words[g]:
                if geo in self.gazetteer_words:
                    weight_g = 1
                elif geo in self.local_words[g]:
                    weight_g = log(self.local_words[g][geo] * self._delta)
                else:
                    weight_g = 0
                # t_count = self._r(geo=geo, tuple_set='bilateral', location=g)
                f_count = self._r(geo=geo, tuple_set='tweet')
                w_g_geo = self._lambda * weight_g * f_count
                g_weights[g] += w_g_geo
        print g_weights
        return max(g_weights.items(), key=lambda x: x[1])

    def _r(self, geo, tuple_set):
        """

        Args:
            geo:
            tuple_set:

        Returns:

        """
        results = 0
        if isinstance(tuple_set, str):
            if tuple_set == 'bilateral':
                print 'bilateral'
            elif tuple_set == 'tweet':
                return self.user['text_nouns'].get(geo, 0)
        return results


if __name__ == "__main__":
    user = {'id': 123, 'location': 'Austin', 'text_nouns': {'word1': 2, 'word2': 1}}
    local_words = {'Austin': {'word1': 0.3, 'word2': 0.12}, 'Chicago': {'word1': 0.5, 'word2': 0.51},
                   'Denver': {'word1': 0.83, 'word2': 0.32}, 'Los Angeles': {'word1': 0.2, 'word2': 0.1},
                   'Las Vegas': {'word1': 0.98, 'word2': 0.87}, 'Miami': {'word1': 0.33, 'word2': 0.32},
                   'New York': {'word1': 0.75, 'word2': 0.12}, 'Portland': {'word1': 0.73, 'word2': 0.52},
                   'Seattle': {'word1': 0.13, 'word2': 0.32}, 'San Fransisco': {'word1': 0.21, 'word2': 0.11}}
    geo_words = {'Austin': {'Austin', 'word1', 'word2'}, 'Chicago': {'Chicago', 'word1', 'word2'},
                 'Denver': {'Denver', 'word1', 'word2'},
                 'Los Angeles': {'Los Angeles', 'word1', 'word2'},
                 'Las Vegas': {'Las Vegas', 'word1', 'word2'}, 'Miami': {'Miami', 'word1', 'word2'},
                 'New York': {'New York', 'word1', 'word2'},
                 'Portland': {'Portland', 'word1', 'word2'}, 'Seattle': {'Seattle', 'word1', 'word2'},
                 'San Fransisco': {'San Fransisco', 'word1', 'word2'}}
    loc_inf = LocationInference(user=user, local_words=local_words, geo_words=geo_words)
    print loc_inf.get_location()
