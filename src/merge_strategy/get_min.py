from merge_strategy.merge_strategy import MergeStrategy

class GetMin(MergeStrategy):
    """
    This class implements a merge strategy that gets the minimum value from a list of integers.
    """

    def merge(self, elements: list) -> int:
        """
        Gets the minimum value from a list of integers.
        If the list is empty or None, raises a ValueError.
        If all elements in the list are string it converts them to integers.

        :param elements: A list of integers to be merged.
        :return: The minimum value.
        """
        if not elements:
            raise ValueError("The given list of GetMin was None or empty.")
        
        # If all elements are strings then it converts them to integers
        if all(isinstance(element, str) for element in elements):
            elements = [int(x) for x in elements]
        
        min_value = min(elements)    
        return min_value