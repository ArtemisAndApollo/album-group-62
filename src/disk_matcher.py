from match_logics.match_logic import MatchLogic
from outputs.output import save_to_csv

class DiskMatcher():
    def __init__(self, modes: dict, debug = False):
        self.debug = debug
        self.modes = modes

    def set_mode(self, mode):
        if mode in self.modes.keys():
            self.mode = mode
            self.sim_function = self.modes[self.mode]["sim_function"]
            self.threshold = self.modes[self.mode]["threshold"]
        else:
            raise ValueError(f"Not a valid mode ({mode}). Valid modes are: {'\n'.join(self.modes.keys())}")
    
    def create_and_save_matches_with_all_modes(self, filepath, entries: list, attributes: list, logic: MatchLogic, with_timestamp=False, timestamp_value=None) -> list:
        matches_paths = []
        for mode in self.modes.keys():
            self.set_mode(mode)
            match = self.get_matches(entries, mode, attributes, logic)
            path = self.save_matches(filepath, match, with_timestamp=with_timestamp, timestamp_value=timestamp_value)
            matches_paths.append(path)
        return matches_paths

    def get_matches(self, entries: list, mode: str, attributes: list, logic: MatchLogic) -> list:
        self.set_mode(mode)

        # There is atleast one entry and the all the attributes are present in the entries keys
        if entries:
            missing = [attr for attr in attributes if attr not in entries[0]]
            if missing:
                raise ValueError(f"Missing attributes in CDDB entries: {', '.join(missing)}")

        matches = []
        for i in range(len(entries)):
            cddb_main = entries[i]

            for j in range(i+1, len(entries)):
                cddb_match = entries[j]

                sim_scores = []
                for attribute in attributes:
                    sim_score = self._check_threshold(cddb_main[attribute], cddb_match[attribute])
                    sim_scores.append(sim_score)

                match_score = logic.compute(sim_scores)

                if match_score != 0:
                    match_line = {
                        "id_0": cddb_main["id"],
                        "cid_0": cddb_main["cid"],
                        "id_1": cddb_match["id"],
                        "cid_1": cddb_match["cid"]
                        # "sim": sim_score
                    }
                    matches.append(match_line)

        return matches            

    def save_matches(self, filepath, matches, with_timestamp=False, timestamp_value=None) -> str:
        ids = ["id_0", "cid_0", "id_1", "cid_1"]

        flattened_matches = []

        for match in matches:
            flattened_match = \
            {
                key: (";".join(match[key]) if key in {'cid_0', 'cid_1'} else match[key])
                for key in match
            }
            flattened_matches.append(flattened_match)
        filepath = filepath + f"_{self.mode}"
        save_to_csv(filepath, ids, flattened_matches, with_timestamp=with_timestamp, timestamp_value=timestamp_value)
        return filepath+".csv"

    def _check_threshold(self, s1: str, s2: str, custom_threshold: float = None):
        sim = self._compute_similarity(s1, s2)
        if self.debug: print(f"Computed similarity is: {sim}")
                             
        if custom_threshold is not None and custom_threshold >= 0.0 and custom_threshold <= 1.0:
            if self.debug: print(f"Using custom threshold: {custom_threshold}")
            threshold = custom_threshold
        else:
            if self.debug: print(f"Using default threshold: {self.threshold}")
            threshold = self.threshold

        if sim >= threshold:
            if self.debug: print(f"Similarity {sim} is above threshold {threshold}")
            return sim
        else:
            if self.debug: print(f"Similarity {sim} is below threshold {threshold}")
            return 0.0
        
    def _compute_similarity(self, s1: str, s2: str) -> float:
        if self.debug:
            print(f"'{s1}' has been lowered to '{s1.lower()}' and '{s2}' to '{s2.lower()}'")
            print(f"Checking similarity between '{s1.lower()}' and '{s2.lower()}' using mode:", self.mode)
        return self.sim_function.compute(s1.lower(), s2.lower())