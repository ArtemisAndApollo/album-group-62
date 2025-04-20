from similarity_functions.similarity_function import SimilarityFunction
from similarity_functions.soundex_similarity import SoundexSimilarity
from similarity_functions.jaro_winkler_similarity import JaroWinklerSimilarity

class SoundexWithJaroWinkler(SimilarityFunction):
    """
    Soundex algorithm for phonetic similarity with Jaro-Winkler similarity.
    """

    def compute(self, s1: str, s2: str) -> float:
        """
        Compute the Jaro-Winkler similarity of the two string if the Soundex codes are the same.
        1 means identical, 0 means completely different.
        
        :param s1: Input string one
        :param s2: Input string two
        :return: Soundex similarity score based on Jaro-Winkler similarity
        """

        soundex = SoundexSimilarity()
        jaro_winkler = JaroWinklerSimilarity()

        soundex_score = soundex.compute(s1, s2)

        if int(soundex_score) == 1:
            jaro_winkler_similarity = jaro_winkler.compute(s1, s2)
            return jaro_winkler_similarity
        else:
            return soundex_score