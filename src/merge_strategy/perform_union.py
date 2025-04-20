from merge_strategy.merge_strategy import MergeStrategy
from merge_strategy.get_uniques import GetAllUniques

class PerformUnion(MergeStrategy):
    """
    This class implements a merge strategy that performs a union of the lists given.
    """

    def __init__(self, perform_similarity: bool = False, merge_features: dict = None):
        self.perform_similarity = perform_similarity
        self.merge_features = merge_features

    def merge(self, elements: list) -> list:
        """
        Performs a union of the lists given.

        :param elements: A list of list to be merged.
        :return: The union of the lists given.
        """
        
        if not all(isinstance(sublist, list) for sublist in elements):
            raise ValueError(f"The following elements of PerformUnion are not lists: \
                              {[not_list for not_list in elements if not isinstance(not_list, list)]}")

        all_uniques_merger = GetAllUniques(self.merge_features)
        
        if self.perform_similarity:
            all_uniques_merger.set_mode(self.mode)
        else:
            all_uniques_merger.set_mode(None)

        all_elements = [item for sublist in elements for item in sublist]

        uniques = all_uniques_merger.merge(all_elements)
        
        return uniques