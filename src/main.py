from similarity_functions.hamming_distance import HammingDistance
from similarity_functions.jaro_winkler_similarity import JaroWinklerSimilarity
from similarity_functions.levenshtein_distance import LevenshteinDistance
from similarity_functions.soundex_similarity import SoundexSimilarity
from similarity_functions.soundex_with_hamming import SoundexWithHamming
from similarity_functions.soundex_with_levenshtein import SoundexWithLevenshtein
from similarity_functions.soundex_with_jaro_winkler import SoundexWithJaroWinkler
from similarity_functions.weaker_soundex_similarity import WeakerSoundexSimilarity
from similarity_functions.weaker_soundex_with_hamming import WeakerSoundexWithHamming
from similarity_functions.weaker_soundex_with_levenshtein import WeakerSoundexWithLevenshtein
from similarity_functions.weaker_soundex_with_jaro_winkler import WeakerSoundexWithJaroWinkler
from handlers.handler_factory import HandlerFactory
from outputs.output import pretty_print_disk_entries, save_to_json
from disk_matcher import DiskMatcher
from disk_evaluator import DiskEvaluator
from match_logics.or_logic import OrLogic
from disk_merger import DiskMerger
import datetime
from utils.serializer import serialize_similarity_modes
from timeit import default_timer as timer
from disk_plotter import DiskPlotter

if __name__ == "__main__":
    factory = HandlerFactory()
    timestamp_value = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")
    start_time_global = timer()

    sanitization_features = {
        "strip_apostroph": True,
        "replace_amp": True,
        "replace_degree_sign": True,
        "replace_incorrect_apostroph": True,
        "swap_name_with_extra_info": True,
        "remove_corrupted_unicode": True,
        "remove_track_numbers": True,
        "remove_artist_name_in_tracks": True,
        "remove_time_in_tracks": True,
        "replace_number_to_apostrophe": True
    }

    # Temporary apply these features to get better merge results
    merge_features = {
        "skip_unknown_track_titles": {
            "value": True,
            "data": [
                r"Onbekend\s+\(Onbekend\)", 
                r"Skladba\s+\d{1}",
                r"Track\d{2}"
            ]
        },
        "remove_special_characters": {
            "value": True,
            "data": ["!", "@", ",", r"\.",r"\(", r"\)", r"\[", r"\]", r"\{", r"\}", r"\\", r"\|", r"\?", "/", "<", ">", "&", r"\^", "%", r"\$", "#", "~", "`", '"', "'", r"\+", "=", "-", "_", r"\*"]
        },
        "replace_numbers_with_letters": {
            "value": True,
            "data": ["a","b","c","d","e","f","g","h","i","j"]
        },
        "replace_Roman_with_letters": {
            "value": True,
            "data": [
                ("I", "a"), 
                ("II", "b"), 
                ("III", "c"), 
                ("IV", "d")
            ] # Also I in normal sentences will be replaced
        },
        "remove_all_spaces": {
            "value": True,
            "data": [r"\s+"]
        },
        "replace_characters_with_base_form": {
            "value": True,
            "data" : [
                ("á", "a"), ("à", "a"), ("ä", "a"), ("â", "a"), ("ã", "a"), ("å", "a"), ("ā", "a"), ("ă", "a"), ("ą", "a"),
                ("Á", "A"), ("À", "A"), ("Ä", "A"), ("Â", "A"), ("Ã", "A"), ("Å", "A"), ("Ā", "A"), ("Ă", "A"), ("Ą", "A"),

                ("é", "e"), ("è", "e"), ("ë", "e"), ("ê", "e"), ("ē", "e"), ("ė", "e"), ("ę", "e"),
                ("É", "E"), ("È", "E"), ("Ë", "E"), ("Ê", "E"), ("Ē", "E"), ("Ė", "E"), ("Ę", "E"),

                ("í", "i"), ("ì", "i"), ("ï", "i"), ("î", "i"), ("ī", "i"), ("į", "i"), ("ı", "i"),
                ("Í", "I"), ("Ì", "I"), ("Ï", "I"), ("Î", "I"), ("Ī", "I"), ("Į", "I"),

                ("ó", "o"), ("ò", "o"), ("ö", "o"), ("ô", "o"), ("õ", "o"), ("ø", "o"), ("ō", "o"),
                ("Ó", "O"), ("Ò", "O"), ("Ö", "O"), ("Ô", "O"), ("Õ", "O"), ("Ø", "O"), ("Ō", "O"),

                ("ú", "u"), ("ù", "u"), ("ü", "u"), ("û", "u"), ("ū", "u"), ("ů", "u"),
                ("Ú", "U"), ("Ù", "U"), ("Ü", "U"), ("Û", "U"), ("Ū", "U"), ("Ů", "U"),

                ("ñ", "n"), ("ń", "n"), ("ň", "n"),
                ("Ñ", "N"), ("Ń", "N"), ("Ň", "N"),

                ("ç", "c"), ("č", "c"), ("ć", "c"),
                ("Ç", "C"), ("Č", "C"), ("Ć", "C"),

                ("ž", "z"), ("ź", "z"), ("ż", "z"),
                ("Ž", "Z"), ("Ź", "Z"), ("Ż", "Z"),

                ("ś", "s"), ("š", "s"), ("ș", "s"),
                ("Ś", "S"), ("Š", "S"), ("Ș", "S"),

                ("ł", "l"), ("ľ", "l"), ("ĺ", "l"),
                ("Ł", "L"), ("Ľ", "L"), ("Ĺ", "L"),

                ("đ", "d"), ("ð", "d"), ("ď", "d"),
                ("Đ", "D"), ("Ð", "D"), ("Ď", "D"),

                ("þ", "th"), ("Þ", "Th"),
                ("œ", "oe"), ("Œ", "OE"),
                ("æ", "ae"), ("Æ", "AE")
            ]
        }
    }

    similarity_modes = {
            "levenshtein": {
                "sim_function": LevenshteinDistance(),
                "threshold": 0.75
                },
            "jaro-winkler": {
                "sim_function": JaroWinklerSimilarity(),
                "threshold": 0.8
                },
            "hamming": {
                "sim_function": HammingDistance(),
                "threshold": 0.75
                },
            "soundex": {
                "sim_function": SoundexSimilarity(),
                "threshold": 1.0
                },
            "s-levenshtein": {
                "sim_function": SoundexWithLevenshtein(),
                "threshold": 0.75
                },
            "s-jaro-winkler": {
                "sim_function": SoundexWithJaroWinkler(),
                "threshold": 0.8
                },
            "s-hamming": {
                "sim_function": SoundexWithHamming(),
                "threshold": 0.75
                },
            "weaker-soundex": {
                "sim_function": WeakerSoundexSimilarity(),
                "threshold": 1.0
                },
            "ws-levenshtein": {
                "sim_function": WeakerSoundexWithLevenshtein(),
                "threshold": 0.75
                },
            "ws-jaro-winkler": {
                "sim_function": WeakerSoundexWithJaroWinkler(),
                "threshold": 0.8
                },
            "ws-hamming": {
                "sim_function": WeakerSoundexWithHamming(),
                "threshold": 0.75
                }
        }

    # Mining XML file with CDDB entries
    total_items = 477 # Total number is 477
    filepath_cddb_data = "data/cddb_discs2.xml"   # Using this data source because of better encoding
    cddb_handler_all = factory.create("disc", data_path=filepath_cddb_data, total_items=total_items, sanitization_features=sanitization_features)
    cddb_entries_all = cddb_handler_all.get_entries()

    # Printing details. disk_id_length = 3 is ideal for cbbd_discs.xml
    pretty_print_disk_entries(entries=cddb_entries_all, max_entries=10, id_length=3, entry_name="Disk")

    switch_time_data_extraction_to_disk_matcher = timer()

    # Create matches with all modes
    disk_matcher = DiskMatcher(modes=similarity_modes, debug=False)
    matches_path = r"output/matches/matches"

    # select one of the following for Attributes to match
    attributes = ['dtitle']
    # attributes = ['artist']
    # attributes = ['artist', 'dtitle']

    logic = OrLogic() # Logic to use for matching
    matches_paths = disk_matcher.create_and_save_matches_with_all_modes(
        filepath=matches_path, entries=cddb_entries_all,
        attributes=attributes, logic=logic, with_timestamp=False, timestamp_value=timestamp_value
    )

    switch_time_disk_matcher_to_disk_evaluator = timer()

    # Evaluate results
    evaluator = DiskEvaluator(debug=True)
    ground_truth_path = r"output/ground_truth/ground_truth.csv"
    eval_path = f"output/eval/eval_{"-".join(attributes)}"
    evals = []
    for matches_path in matches_paths:
        mode = matches_path.split("_")[1].split(".")[0]
        evaluation = evaluator.evaluate_matches(ground_truth_path=ground_truth_path, matches_path=matches_path, mode = mode, disc_count = total_items)
        evaluation["mode"] = mode
        evals.append(evaluation)
    
    evals.sort(key=lambda x: x["F1-score"], reverse=True) # Rank results by f1-score
    evaluator.save_results(filepath=eval_path, results=evals, with_timestamp=True, timestamp_value=timestamp_value)
    
    switch_time_disk_evaluator_to_disk_merger = timer()

    # Merge matches
    disk_merger = DiskMerger(similarity_modes=similarity_modes, merge_features=merge_features)
    matches_path = rf"output/matches/matches_{evals[0]["mode"]}.csv"
    new_disks_xml_path = r"output/merged/merged"
    disk_merger.create_and_save_merges_with_all_modes(
        cddb_entries=cddb_entries_all, matches_path=matches_path,
        new_disk_xml_path=new_disks_xml_path, with_timestamp=False, timestamp_value=timestamp_value)
    
    # Timing
    end_time_global = timer()
    time_diff_data_extraction = switch_time_data_extraction_to_disk_matcher - start_time_global
    time_diff_disk_matcher = switch_time_disk_matcher_to_disk_evaluator - switch_time_data_extraction_to_disk_matcher
    time_diff_disk_evaluator = switch_time_disk_evaluator_to_disk_merger - switch_time_disk_matcher_to_disk_evaluator
    time_diff_disk_merger = end_time_global - switch_time_disk_evaluator_to_disk_merger
    time_diff_total = end_time_global - start_time_global
    print("Timing per process (in seconds):")
    print("Data extraction: {0:.5f}".format(time_diff_data_extraction))
    print("Disk Matcher:\t {0:.5f}".format(time_diff_disk_matcher))
    print("Disk Evaluator:\t {0:.5f}".format(time_diff_disk_evaluator))
    print("Disk Merger:\t {0:.5f}".format(time_diff_disk_merger))
    print("Total:\t\t {0:.5f}".format(time_diff_total))

    # Save settings
    settings_path = f"output/settings/settings"
    # settings_path = f"output/plots/timing_files_extended/{"-".join(attributes)}/settings"
    process_times_seconds = {
        "data_extraction": time_diff_data_extraction,
        "disk_matcher": time_diff_disk_matcher,
        "disk_evaluator": time_diff_disk_evaluator,
        "disk_merger": time_diff_disk_merger,
        "total": time_diff_total
    }
    data = {
        "timestamp": timestamp_value.strip("_"),
        "sanitization_features": sanitization_features,
        "merge_features": merge_features,
        "matching_attributes": attributes,
        "similarity_modes": serialize_similarity_modes(similarity_modes),
        "process_times_seconds": process_times_seconds
    }
    save_to_json(settings_path,data, with_timestamp=True, timestamp_value=timestamp_value)

    # Plotting
    disk_plotter = DiskPlotter(evals = evals, filename_attributes="-".join(attributes))
    disk_plotter.plot_all_single_tp_fp_tn_fn()
    disk_plotter.plot_all_single_sim_mode()
    disk_plotter.plot_single_timing(process_times = process_times_seconds)
    disk_plotter.plot_all_sim_modes_subplot_excluded_soundex()
    disk_plotter.plot_all_sim_modes_vertical()
    disk_plotter.plot_all_sim_modes_horizontal()
    disk_plotter.plot_multiple_timing()
    disk_plotter.plot_all_tp_fp_tn_fn_stacked_bar()
    # disk_plotter.plot_show_all()