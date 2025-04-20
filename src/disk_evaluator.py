from sklearn.metrics import precision_recall_fscore_support
from outputs.output import save_to_csv

class DiskEvaluator():
    def __init__(self, debug: bool = False):
        self.debug = debug

    def evaluate_matches(self, ground_truth_path: str, matches_path: str, mode: str = None, disc_count: int = 0) -> dict:
        ground_truth = set()
        with open (ground_truth_path,"r") as f:
            for line in f.readlines():
                ids = line.strip().split(",")
                short_ids = ids[0] + "," + ids[2]
                ground_truth.add(short_ids)

        matches = set()
        with open (matches_path,"r") as f:
            for line in f.readlines():
                ids = line.strip().split(",")
                match, match_rev = ids[0] + "," + ids[2], ids[2] + "," + ids[0]
                # Swappes id order if that one is a match
                if match_rev in ground_truth:
                    matches.add(match_rev)
                else:
                    matches.add(match)

        true_positive = len(ground_truth & matches)
        false_negative = len(ground_truth - matches)
        false_positive = len(matches - ground_truth)

        relevant = [1] * true_positive + [1] * false_negative + [0] * false_positive
        predicted = [1] * true_positive + [0] * false_negative + [1] * false_positive

        pre,rec,f1,_ = precision_recall_fscore_support(relevant, predicted, average='binary')

        n_ground_truth = len(ground_truth)
        n_match = len(matches)

        if self.debug:
            if mode is not None:
                print(f"EVALUATION FOR: {mode}\n")

            if disc_count > 1:
                total_count = int((disc_count * (disc_count - 1)) / 2)
                true_negative = total_count - (true_positive + false_negative + false_positive)
            else:
                total_count = 0
                true_negative = 0
            print(f"Number of ground truth: {n_ground_truth}")
            print(f"Number of matches: {n_match}")
            if disc_count > 1: print(f"Possible number of matches: {total_count}")
            print(f"True positives: {true_positive}")
            print(f"False positives: {false_positive}")
            if disc_count > 1: print(f"True negatives: {true_negative}")
            print(f"False negatives: {false_negative}")
            print(f"Ground truth + Matches = {n_ground_truth + n_match}")
            print(f"True positives * 2 + False positives + False negatives = {true_positive*2 + false_positive + false_negative}")
            print("Precision: ",pre,"\nRecall: ",rec,"\nF1 score: ",f1, "\n")
            # print(f"False positive samples: {matches - ground_truth}")
            # print(f"False negative samples: {ground_truth - matches}")
            
        result = {"precision":pre,
                "recall":rec,
                "F1-score":f1,
                "ground_truth":n_ground_truth,
                "matches":n_match,
                "tp":true_positive,
                "fp":false_positive,
                "tn":true_negative,
                "fn":false_negative,
                "total":total_count
                }
        
        if mode is not None:
            result["mode"] = mode

        return result
    
    def save_results(self, filepath: str, results: list, with_timestamp: bool = True, timestamp_value=None):
        save_to_csv(filepath, ["mode", "precision", "recall",
                                "F1-score", "ground_truth",
                                "matches", "tp", "fp", "tn", "fn", "total"], results,
                                display_header=True, with_timestamp=with_timestamp, timestamp_value=timestamp_value)

