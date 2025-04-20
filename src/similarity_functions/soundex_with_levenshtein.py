from similarity_functions.similarity_function import SimilarityFunction
from similarity_functions.soundex_similarity import SoundexSimilarity
from similarity_functions.levenshtein_distance import LevenshteinDistance

class SoundexWithLevenshtein(SimilarityFunction):
    """
    Soundex algorithm for phonetic similarity with Levenshtein distance.
    """

    def compute(self, s1: str, s2: str) -> float:
        """
        Compute the Levenshtein distance of the two string if the Soundex codes are the same.
        1 means identical, 0 means completely different.
        
        :param s1: Input string one
        :param s2: Input string two
        :return: Soundex similarity score based on Levenshtein distance
        """

        soundex = SoundexSimilarity()
        levenshtein = LevenshteinDistance()

        soundex_score = soundex.compute(s1, s2)

        if int(soundex_score) == 1:
            levenshtein_distance = levenshtein.compute(s1, s2)
            return levenshtein_distance
        else:
            return soundex_score