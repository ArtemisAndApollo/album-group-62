from merge_strategy.merge_strategy import MergeStrategy
from similarity_functions.similarity_function import SimilarityFunction
import re

class GetAllUniques(MergeStrategy):
    """
    This class implements a merge strategy that gets all the unique elements of the given list.
    """
    def __init__(self, merge_features: dict = None):
        self.merge_features = merge_features

    def merge(self, elements: list[str]) -> list:
        """
        Gets all the unique elements from a list of elements.
        If the list is empty or None, raises a ValueError.

        :param elements: A list of elements to be merged.
        :return: The set of the elements.
        """
        
        if not elements:
            raise ValueError("The given list of GetAllUniques was None or empty.")
        
        if self.mode:
            similarity_function: SimilarityFunction = self.mode["sim_function"]
            threshold = self.mode["threshold"]
            uniques: list[str] = []
            for element in elements:
                not_in_uniques = True
                for unique in uniques:
                    s1 = element.lower()
                    s2 = unique.lower()
                    
                    s1, s2 = self._check_merge_features(s1, s2)

                    if similarity_function.compute(s1, s2) >= threshold:
                        not_in_uniques = False
                        break
                if not_in_uniques:
                    uniques.append(element)
                                
            return uniques
            
        else:
            return list(set(elements))
        

    def _check_merge_features(self, s1: str, s2: str) -> tuple[str, str]:
        if self.merge_features is not None:
            if "skip_unknown_track_titles" in self.merge_features and self.merge_features["skip_unknown_track_titles"]["value"]:
                s1, s2 = self._skip_unknown_track_titles(s1, s2)
            if "remove_special_characters" in self.merge_features and self.merge_features["remove_special_characters"]["value"]:
                s1, s2 = self._remove_special_characters(s1, s2)
            if "replace_numbers_with_letters" in self.merge_features and self.merge_features["replace_numbers_with_letters"]["value"]:
                s1, s2 = self._replace_numbers_with_letters(s1, s2)
            if "replace_Roman_with_letters" in self.merge_features and self.merge_features["replace_Roman_with_letters"]["value"]:
                s1, s2 = self._replace_Roman_with_letters(s1, s2)
            if "remove_all_spaces" in self.merge_features and self.merge_features["remove_all_spaces"]["value"]:
                s1, s2 = self._remove_all_spaces(s1, s2)

        return s1, s2
    
    def _remove_special_characters(self, s1: str, s2: str) -> tuple[str, str]:
        return self._base_merge_check(s1, s2, "remove_special_characters")
            
    def _replace_numbers_with_letters(self, s1: str, s2: str) -> tuple[str, str]:
        alphabet = self.merge_features["replace_numbers_with_letters"]["data"]
        for i, letter in enumerate(alphabet):
            s1 = s1.replace(str(i), letter)
            s2 = s2.replace(str(i), letter)
        return s1, s2
    
    def _replace_Roman_with_letters(self, s1: str, s2: str) -> tuple[str, str]:
        data = self.merge_features["replace_Roman_with_letters"]["data"]
        for letter, replacement in data:
            re.sub(rf"\b({letter})\b", replacement, s1)
            re.sub(rf"\b({letter})\b", replacement, s2)
        return s1, s2


    def _skip_unknown_track_titles(self, s1: str, s2: str) -> tuple[str, str]:
        return self._base_merge_check(s1, s2, "skip_unknown_track_titles")

    def _remove_all_spaces(self, s1: str, s2: str) -> tuple[str, str]:
        return self._base_merge_check(s1, s2, "remove_all_spaces")
    
    def _replace_characters_with_base_form(self, s1: str, s2: str) -> tuple[str, str]:
        data = self.merge_features["replace_characters_with_base_form"]["data"]
        for letter, replacement in data:
            re.sub(letter, replacement, s1)
            re.sub(letter, replacement, s2)
        return s1, s2
    
    def _base_merge_check(self, s1: str, s2: str, key: str) -> tuple[str, str]:
        data = self.merge_features[key]["data"]
        for entry in data:
            re.sub(entry, "", s1)
            re.sub(entry, "", s2)
        return s1, s2