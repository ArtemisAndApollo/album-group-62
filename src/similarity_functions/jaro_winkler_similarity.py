from similarity_functions.similarity_function import SimilarityFunction
from jellyfish import jaro_winkler_similarity

class JaroWinklerSimilarity(SimilarityFunction):
    """
    Jaro-Winkler similarity function.
    """

    def compute(self, s1: str, s2: str) -> float:
        """
        Compute the Jaro-Winkler similarity between two strings.
        1 means identical, 0 means completely different.

        :param a: First string
        :param b: Second string
        :return: Jaro-Winkler similarity score
        """

        if s1 == "" and s2 == "":
            return 1.0
        
        return jaro_winkler_similarity(s1, s2)
