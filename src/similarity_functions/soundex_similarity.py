from similarity_functions.similarity_function import SimilarityFunction
from jellyfish import soundex

class SoundexSimilarity(SimilarityFunction):
    """
    Soundex algorithm for phonetic similarity.
    """

    def compute(self, s1: str, s2: str) -> float:
        """
        Compute the Soundex similarity for a given string.
        1 means identical, 0 means completely different.

        :param s1: Input string one
        :param s2: Input string two
        :return: Soundex similarity score
        """
        soundex_s1 = soundex(s1)
        soundex_s2 = soundex(s2)
        return 1.0 if soundex_s1 == soundex_s2 else 0.0