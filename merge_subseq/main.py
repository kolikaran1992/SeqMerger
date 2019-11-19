from nltk.tokenize import RegexpTokenizer
from .__common__ import LOGGER_NAME
import logging

logger = logging.getLogger(LOGGER_NAME)

from .lcs import LongestContiguousSubSeq


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
        lcs = LongestContiguousSubSeq(s1=self._tokenizer.tokenize(s1),
                                      s2=self._tokenizer.tokenize(s2))
        obj = lcs.main()

        s1_common_tok_idxs = [item for item, _ in obj]
        s2_common_tok_idxs = [item for _, item in obj]
