from similarity_functions.similarity_function import SimilarityFunction
from jellyfish import hamming_distance

class HammingDistance(SimilarityFunction):
    """
    Hamming distance similarity function.
    """

    def compute(self, s1: str, s2: str) -> float:
        """
        Compute the normalized Hamming distance between two strings.
        1 means identical, 0 means completely different.
        
        :param a: First string
        :param b: Second string
        :return: Normalized Hamming distance
        """
        sim = hamming_distance(s1, s2)
        l1, l2 = len(s1), len(s2)
        max_len = max(l1, l2)
        if max_len == 0: return 1.0
        norm_sim = 1 - (sim / max_len)
        return norm_sim