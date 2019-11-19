from .__common__ import LOGGER_NAME
import logging

logger = logging.getLogger(LOGGER_NAME)


class LongestContiguousSubSeq(object):
    """
    --> find longest contiguous subsequence
    """

    def __init__(self,
                 s1=(),
                 s2=()):
        """
        :param s1 (list): list of tokens
        :param s2 (list): list of tokens
        """
        if not s1:
            logger.warning('sequence 1 is empty')
        if not s2:
            logger.warning('sequence 2 is empty')
        self._s1 = s1
        self._s2 = s2

        logger.info('sequence 1 is "{}" tokens long and sequence 2 is {} tokens long'.format(len(s1), len(s2)))

        ## elements of s1 will represent rows
        ## elements of s2 will represent columns
        ## len + 1 represents null element at the start of each seq
        self._memory = [[0 for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]

    def _populate_memory(self):
        if not self._s1 or not self._s2:
            logger.warning(
                'since one of the sequence is 0 tokens long, therefore the memory matrix will not be populated')
            return

        ## start from top left corner
        for i in range(len(self._s1) + 1):
            for j in range(len(self._s2) + 1):
                if i == 0 or j == 0:
                    self._memory[i][j] = 0
                elif self._s1[i - 1] == self._s2[j - 1]:
                    self._memory[i][j] = self._memory[i - 1][j - 1] + 1
                else:
                    self._memory[i][j] = max(self._memory[i - 1][j], self._memory[i][j - 1])

        logger.info('successfully populated lcs memory')

    def main(self):
        """
        :return (list): list of tuples
                    --> each tuple will contain the index of common token (w.r.t. s1, w.r.t. s2)
                    --> return [] in case of no common contiguous sequence
        """
        if not self._s1 or not self._s2:
            logger.info('since one of the sequence is 0 tokens long, therefore returning []')
            return []

        self._populate_memory()

        i = len(self._s1)
        j = len(self._s2)

        ret_obj = []

        while i > 0 and j > 0:

            # If current character in X[] and Y are same, then
            # current character is part of LCS
            if self._s1[i - 1] == self._s2[j - 1]:
                ret_obj.append((i - 1, j - 1))
                i -= 1
                j -= 1

            # If not same, then find the larger of two and
            # go in the direction of larger value
            elif self._memory[i - 1][j] > self._memory[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return sorted(ret_obj, key=lambda x: x[0])
