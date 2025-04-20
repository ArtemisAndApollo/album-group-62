from match_logics.match_logic import MatchLogic

class OrLogic(MatchLogic):
    """
    Class for OR logic matching.
    """

    def compute(self, scores: list) -> float:
        """
        Computes the OR matching score for a list of similarity scores.
        The OR logic returns the maximum score from the list of similarity scores.

        :param scores: List of similarity scores
        :return: OR Matching score
        """

        max_score = max(scores)

        return max_score