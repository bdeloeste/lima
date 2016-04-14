"""
TFDFIDF Algorithm
Author: Bryan Deloeste

Source: http://www.jcomputers.us/vol9/jcp0902-09.pdf
"""
from collections import defaultdict
from difflib import SequenceMatcher
from math import log
from nltk import pos_tag
from nltk.tokenize import TweetTokenizer


class TFDFIDF(object):
    """
    Insert docstring
    """

    def __init__(self, corpus, all_nouns):
        """

        Args:
            corpus: { 'location': tweet['user']['location'],
                      'bilateral_friends_location_occurrences': loc_occurrence_count,
                      'text_nouns': tweet_nouns }
        """
        self.corpus = corpus
        self.gazetteer_words = {'Austin', 'Chicago', 'Denver', 'Los Angeles', 'Las Vegas', 'Miami', 'New York',
                                'Portland', 'Seattle', 'San Fransisco'}
        self.all_nouns = all_nouns
        self._similarity_threshold = 0.7

    def tfdfidf(self):
        """

        Args:
            user:
            tweets:
            location:

        Returns:

        """
        G = len(self.gazetteer_words)
        for g in self.gazetteer_words:
            for noun in self.all_nouns:
                Ng_n = self._ng_n(noun=noun, location=g)
                Ng = self._ng(location=g)
                if Ng == 0:
                    continue
                tf = Ng_n / Ng
                Ug_n = self._ug_n(noun=noun, location=g)
                Ug = self._ug(location=g)
                df = float(len(Ug_n))/float(len(Ug))
                NLg = self._nlg_n(noun=noun, location=g)
                idf = log(G / (1 + NLg))
                tfdfidf = tf * df * idf
                print g, ':', noun, ': ', 'tfdfidf: ', tfdfidf

    def _ng_n(self, noun, location):
        """
        Ng(noun) denotes noun n's appearance number when location is g
        Args:
            noun:

        Returns:

        """
        noun_appearing_number = 0
        for value in self.corpus.itervalues():
            if self._similarity_ratio(value['location'], location) > self._similarity_threshold:
                noun_appearing_number += value['text_nouns'][noun]
        return float(noun_appearing_number)

    def _ng(self, location):
        """
        Ng denotes all nouns in users' tweets when location is g
        Returns:

        """
        Ng = 0
        for value in self.corpus.itervalues():
            if self._similarity_ratio(value['location'], location) > self._similarity_threshold:
                for n in value['text_nouns'].itervalues():
                    Ng += n
        return float(Ng)

    def _nlg_n(self, noun, location):
        """

        Args:
            noun:
            location:

        Returns:

        """
        location_number = 0
        for value in self.corpus.itervalues():
            if self._similarity_ratio(value['location'], location) > self._similarity_threshold:
                if value['text_nouns'][noun] > 0:
                    location_number += 1
        return float(location_number)

    def _ug_n(self, noun, location):
        """

        Args:
            noun:
            location:

        Returns:

        """
        users = []
        for key, value in self.corpus.iteritems():
            if self._similarity_ratio(value['location'], location) > self._similarity_threshold \
                    and value['text_nouns'][noun] > 0:
                users.append(key)
        return users

    def _ug(self, location):
        """

        Args:
            location:

        Returns:

        """
        users = []
        for key, value in self.corpus.iteritems():
            if self._similarity_ratio(value['location'], location) > self._similarity_threshold:
                users.append(key)
        return users

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

    @staticmethod
    def _get_nouns(tweet_text):
        """

        Args:
            tweet_text:

        Returns:

        """
        tokenizer = TweetTokenizer()
        nouns = []
        for tweet in tweet_text:
            tag = pos_tag(tokenizer.tokenize(tweet))
            nouns.extend([t[0] for t in tag if t[1] == 'NN'])
        return nouns


if __name__ == '__main__':
    test1, test2, test3 = defaultdict(int), defaultdict(int), defaultdict(int)
    test1['nice'] = 2
    test1['good'] = 5
    test1['eat'] = 1
    test2['word'] = 3
    test2['nice'] = 5
    test3['okay'] = 9
    nouns = {'nice', 'good', 'eat', 'word', 'okay'}
    test_corpus = {
        123: {
            'location': 'Austin',
            'bilateral_friend_location_occurrences': None,
            'text_nouns': test1
        },
        234: {
            'location': 'Austin',
            'bilateral_friend_location_occurrences': None,
            'text_nouns': test2
        },
        235: {
            'location': 'Miami',
            'bilateral_friend_location_occurrences': None,
            'text_nouns': test3
        }
    }
    tfdfidf = TFDFIDF(corpus=test_corpus, all_nouns=nouns)
    tfdfidf.tfdfidf()
