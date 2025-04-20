from similarity_functions.similarity_function import SimilarityFunction
from similarity_functions.soundex_similarity import SoundexSimilarity
from similarity_functions.hamming_distance import HammingDistance

class SoundexWithHamming(SimilarityFunction):
    """
    Soundex algorithm for phonetic similarity with Hamming distance.
    """

    def compute(self, s1: str, s2: str) -> float:
        """
        Compute the Hamming distance of the two string if the Soundex codes are the same.
        1 means identical, 0 means completely different.
        
        :param s1: Input string one
        :param s2: Input string two
        :return: Soundex similarity score based on Hamming distance
        """

        soundex = SoundexSimilarity()
        hamming = HammingDistance()

        soundex_score = soundex.compute(s1, s2)

        if int(soundex_score) == 1:
            hamming_distance = hamming.compute(s1, s2)
            return hamming_distance
        else:
            return soundex_score
