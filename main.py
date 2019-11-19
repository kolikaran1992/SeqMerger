from nltk.tokenize import RegexpTokenizer
from .__common__ import LOGGER_NAME
import logging
logger = logging.getLogger(LOGGER_NAME)

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

        if 'span_tokenize' not in [func for func in dir(tokenizer) if callable(getattr(tokenizer, func))]:
            logger.error('the tokenizer should have the method span_tokenize, which works as nltk.RegexpTokenizer.span_tokenize')
            exit(1)

        self._tokenizer = tokenizer
        logger.info('tokenizer set successfully')

