from nltk.tokenize import RegexpTokenizer
from .__common__ import LOGGER_NAME
import logging
from .lcs import LongestContiguousSubSeq
from functools import reduce

logger = logging.getLogger(LOGGER_NAME)


class MergeSubSeq(object):
    """
    --> given two string sequences (char or words)
    --> return pairwise insertion and deletion in sequence given the its updated version
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
        a = [(None, None)] + l
        return list(zip(a[:-1], a[1:]))

    @staticmethod
    def __process_item(a, b):
        """
        --> return idxs
        :param a (int or None): token idx
        :param b (int or None): token idx
        :return (list): list of token idxs between range a(not included if a is not None else included), b
        """
        return list(range(0, b)) if a is None else list(range(a + 1, b))

    @staticmethod
    def __process_tuple(prev_tup, tup):
        """
        --> returns list of idxs between prev_tup[i], tup[i] ; i = 0, 1
        :param tup (int, int): (tok idx of seq 1, tok idx of seq 2)
        :param prev_tup (tuple): (a, b), where a, b can be int or None
        :return (tuple): (list, list) :: (deletion token idxs, insertion token idxs)
        """
        idxs_a = MergeSubSeq.__process_item(prev_tup[0], tup[0])
        idxs_b = MergeSubSeq.__process_item(prev_tup[1], tup[1])

        ins_idx = idxs_a[-1] if idxs_a else prev_tup[0] if prev_tup[0] else -1

        return (idxs_a, idxs_b, ins_idx)

    def extract(self, s1, s2):
        """
        --> returns changes in s1 considering s2 is updated version of s1
        :param s1 (str): sequence
        :param s2 (str): updated sequence
        :return (list): list of dictionaries
                        -> dictionary structure : {'deletion': (int, int), 'insertion': list}
        """
        s1_tokens = self._tokenizer.tokenize(s1)
        s2_tokens = self._tokenizer.tokenize(s2)

        s1_spans = list(self._tokenizer.span_tokenize(s1))

        lcs = LongestContiguousSubSeq(s1=s1_tokens,
                                      s2=s2_tokens)
        obj = lcs.main()
        changes = []
        for tup_a, tup_b in MergeSubSeq.__combine(obj):
            del_idxs, ins_idxs, ins_tok_pos = MergeSubSeq.__process_tuple(tup_a, tup_b)
            ins_tokens = [s2_tokens[idx] for idx in ins_idxs] if ins_idxs else None
            deletion = (s1_spans[del_idxs[0]][0], s1_spans[del_idxs[-1]][1]) if del_idxs else None

            ins_pos = s1_spans[ins_tok_pos][
                1] if ins_tok_pos is not None and ins_tok_pos != -1 else 0 if ins_tok_pos == -1 else None

            if ins_tok_pos is None and ins_tokens:
                logger.warning('"{}" has insertion tokens but no insertion position'.format(s1))

            changes.append({'deletion': deletion,
                            'insertion': {'tokens': ins_tokens,
                                          'position': ins_pos} if ins_tokens else None})

        return list(filter(lambda x: reduce(lambda a, b: a or b
                                            , x.values()), changes))
