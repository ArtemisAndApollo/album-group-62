from merge_strategy.get_uniques import GetAllUniques
from merge_strategy.merge_strategy import MergeStrategy

class GetAllUniquesExclude(MergeStrategy):
    """
    This class implements a merge strategy that gets all the unique elements
    except the ones given in the constructor.
    """

    def __init__(self, exclude: list = None):
        if exclude is None:
            exclude = {}

        self.exclusions = set(exclude)

    def merge(self, elements: list) -> list:
        """
        Gets all the unique elements from a list of elements except the ones on the exclusion list.
        If all the elements are on the exclusion list, then returns a random element from the exclusion list.

        :param elements: A list of elements to be merged.
        :return: The set of the elements except the ones on the exclusion list.
        """
        
        all_uniques_merger = GetAllUniques()
        all_uniques_merger.set_mode(None)

        uniques = all_uniques_merger.merge(elements)

        if self.exclusions:
            accepted_elements = list(set(uniques) - self.exclusions)
        
            # If all the elements on the list are exluded
            if not accepted_elements:
                return uniques[0] # Return the first element of the uniques list
            
            uniques = accepted_elements
        
        return uniques