class SimilarityFunction:
    """
    Abstract base class for similarity functions.
    """

    def compute(self, s1: str, s2: str) -> float:
        """
        Computes string similarity of the two strings.

        :param a: First string
        :param b: Second string
        :return: Similarity score
        """
        raise NotImplementedError("Subclasses should implement this method.")