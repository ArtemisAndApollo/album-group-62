from similarity_functions.similarity_function import SimilarityFunction

class MergeStrategy:

    def set_mode(self, mode: dict):
        """
        Sets the similarity mode for the merging strategy.
        
        :param mode: The similarity mode to be used.
        """
        self.mode = mode

    def merge(self, elements: list) -> list:
        """
        Defines the merging strategy for the given attribute of a set of disk entries.
        
        :param elements: A list of elements to be merged.
        :return: The merged result.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")