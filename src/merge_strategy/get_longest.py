from merge_strategy.merge_strategy import MergeStrategy

class GetLongest(MergeStrategy):
    """
    This class implements a merge strategy that gets the longest string from a list of strings.
    """

    def merge(self, elements: list) -> str:
        """
        Gets the longest string from a list of strings.
        If the list is empty or None, raises a ValueError.
        If any element in the list is not a string, raises a ValueError.

        :param elements: A list of strings to be merged.
        :return: The longest string.
        """
        if not elements:
            raise ValueError("The given list of GetLongest was None or empty.")
        
        if not all(isinstance(i, str) for i in elements):
            raise ValueError(f"The following elements of GetLongest are not strings: \
                              {[not_str for not_str in elements if not isinstance(not_str, str)]}")
        
        longest_string = max(elements, key=len)    
        return longest_string 