from similarity_functions.similarity_function import SimilarityFunction
from jellyfish import soundex

class WeakerSoundexSimilarity(SimilarityFunction):
    """
    Weaker Soundex algorithm for phonetic similarity.
    """

    def compute(self, s1: str, s2: str) -> float:
        """
        Compute the Weaker Soundex similarity for a given string.
        If the soundex codes are different then checks for soundex scores of the first words.
        If the first word is 'the' then it checks the second word.
        1 means identical, 0 means completely different.

        :param s1: Input string one
        :param s2: Input string two
        :return: Weaker Soundex similarity score
        """
        soundex_s1 = soundex(s1)
        soundex_s2 = soundex(s2)
        
        if soundex_s1 == soundex_s2:
            return 1.0
        
        s1_splits = s1.split(" ")
        s2_splits = s2.split(" ")

        s1_split = s1_splits[0]
        s2_split = s2_splits[0]

        if s1_split == "the" and len(s1_splits) >= 2:
            s1_split = s1.split(" ")[1]

        if s2_split == "the" and len(s2_splits) >= 2:
            s2_split = s2.split(" ")[1]

        return 1.0 if soundex(s1_split) == soundex(s2_split) else 0.0