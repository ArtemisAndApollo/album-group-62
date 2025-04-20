class MatchLogic:
    """
    Abstract base class for matching logics.
    """

    def compute(self, scores: list) -> float:
        """
        Computes the matching score for a list of similarity scores

        :param scores: List of similarity scores
        :return: Matching score
        """
        raise NotImplementedError("Subclasses should implement this method.")