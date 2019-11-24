from nltk.tokenize import RegexpTokenizer
from .__common__ import LOGGER_NAME
import logging

logger = logging.getLogger(LOGGER_NAME)

from .lcs import LongestContiguousSubSeq
from functools import reduce


class MergeSubSeq(object):
    """
    --> given two string sequences (char or words)
    --> merge common sub sequences
    """

    def __init__(self,
                 tokenizer=None):
        if not tokenizer:
            logger.info('Using default tokenizer')
            self._tokenizer = RegexpTokenizer(r'\w+|[^\w\s]')
        else:
            self._tokenizer = tokenizer

        if not callable(getattr(self._tokenizer, 'span_tokenize', None)):
            logger.error(
                'the tokenizer should have the method span_tokenize, which works as nltk.RegexpTokenizer.span_tokenize')
            exit(1)

        logger.info('tokenizer set successfully')

    @staticmethod
    def __combine(l):
        """
        --> selects two consecutive elements of the list and send the output to a new list
        --> [a,b,c,d] will be converted to [(O,a), (a,b), (b,c), (c,d)]
            where a,b,c and d are tuples and O is 0 tuple (0, 0)
        :param l (list): list of tuples
        :return (list): as explained above
        """
        if len(l) == 1:
            return [((0, 0), l[0])]

        return list(zip([(0, 0)] + l[:-1], [(0, 0)] + l[1:]))

    def extract(self, s1, s2, return_tokens=False):
        """
        --> returns common sub sequence from s1 and s2
        :param s1 (str): first sequence
        :param s2 (str): second sequence
        :return (list): list of dictionaries
                        -> dictionary structure : {'text': str, 'sequence': str}
                           the key 'sequence' can be:
                                            's1' if text belongs to sequence 1
                                            's2' if text belongs to sequence 2
                                            'common' if text belongs to both
        """
        s1_tokens = self._tokenizer.tokenize(s1)
        s2_tokens = self._tokenizer.tokenize(s2)
        s1_spans = list(self._tokenizer.span_tokenize(s1))
        lcs = LongestContiguousSubSeq(s1=s1_tokens,
                                      s2=s2_tokens)
        obj = lcs.main()
        changes = []
        if not obj:
            logger.info('nothing is common between the two sequences')
            changes = [{'deletion': {'tokens': s1_tokens, 'span': (s1_spans[0][0], s1_spans[-1][1])},
                        'insertion': {'tokens': s2_tokens, 'position': s1_spans[-1][1]}
                        }]
        else:
            for tup_a, tup_b in MergeSubSeq.__combine(obj):
                _del = [idx for idx in range(tup_a[0] + 1, tup_b[0])]
                _t = [s2_tokens[idx] for idx in range(tup_a[1] + 1, tup_b[1])]
                insertion = {'tokens': _t, 'position': s1_spans[tup_b[0]][0]} if _t else None
                deletion = {'tokens': [s1_tokens[idx] for idx in _del],
                            'span': (s1_spans[_del[0]][0], s1_spans[_del[-1]][1])} if _del else None
                pair = {'deletion': deletion, 'insertion': insertion}
                changes += [pair]

                changes = list(filter(lambda x: reduce(lambda a, b: a or b, x.values()), changes))

        changes = [{'deletion': item['deletion']['span'] if item['deletion'] else None,
                    'insertion': item['insertion']['tokens'] if item['insertion'] else None} for item in changes]

        logger.info('successfully extracted changes')

        return changes
