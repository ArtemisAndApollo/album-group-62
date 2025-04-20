from similarity_functions.similarity_function import SimilarityFunction
from jellyfish import levenshtein_distance

class LevenshteinDistance(SimilarityFunction):
    """
    Levenshtein distance similarity function.
    """

    def compute(self, s1: str, s2: str) -> float:
        """
        Compute the normalized Levenshtein distance between two strings.
        1 means identical, 0 means completely different.

        :param s1: First string
        :param s2: Second string
        :return: Normalized Levenshtein similarity score
        """
        sim = levenshtein_distance(s1, s2)
        l1, l2 = len(s1), len(s2)
        max_len = max(l1, l2)
        if max_len == 0: return 1.0
        norm_sim = 1 - (sim / max_len)
        return norm_sim