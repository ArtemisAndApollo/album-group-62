import networkx as nx
from xml.dom.minidom import Document
from outputs.output import save_to_xml
from merge_strategy.get_longest import GetLongest
from merge_strategy.get_min import GetMin
from merge_strategy.get_uniques_exclude import GetAllUniquesExclude
from merge_strategy.perform_union import PerformUnion

class DiskMerger:
    def __init__(self, similarity_modes: dict, merge_features: dict = None):
        self.similarity_modes = similarity_modes
        self.strategies = {
            "id": GetMin(),
            "cid": PerformUnion(),
            "artist": GetLongest(),
            "dtitle": GetLongest(),
            "category": GetAllUniquesExclude(exclude=["misc", "data"]),
            "tracks": PerformUnion(perform_similarity=True, merge_features=merge_features)
        }

    def get_merge_strategy_names(self) -> set:
        return set(self.strategies.keys())

    def _load_matches(self, matches_path: str) -> set:
        matches = set()
        with open (matches_path,"r") as f:
            for line in f.readlines():
                ids = line.strip().split(",")
                match = (ids[0], ids[2])
                matches.add(match)
        return matches

    def _get_merge_groups(self, matches: set) -> list:
        match_graph = nx.Graph()
        match_graph.add_edges_from(matches)
        merge_groups = list(nx.connected_components(match_graph))
        return merge_groups
    
    def _get_attribute_set(self, cddb_entries: list) -> set:
        # Get a set of all keys of the cddb entries
        attributes = {key for entry in cddb_entries for key in entry}
        return attributes

    def _merge_entries_in_groups(self, merge_groups_ids: list, cddb_entries: list, similarity_mode: dict) -> list:
        merged_entries = []

        for merge_group_ids in merge_groups_ids:
            merge_group = [entry for entry in cddb_entries if entry["id"] in merge_group_ids]
            attributes = self._get_attribute_set(merge_group)
            
            unrecognised_attributes = attributes - self.get_merge_strategy_names()
            if unrecognised_attributes:
                raise ValueError(f"There are no merging strategies for the following attributes: {unrecognised_attributes}")

            merged_entry = dict()
            for attribute in attributes:
                merge_group_attributes = [entry[attribute] for entry in merge_group]
                merge_strategy = self.strategies[attribute]
                merge_strategy.set_mode(similarity_mode)
                merged_value = merge_strategy.merge(merge_group_attributes)
                merged_entry[attribute] = merged_value
            
            merged_entries.append(merged_entry)

        return merged_entries

    def _add_not_duplicates(self, merged_entries: list, cddb_entries: list, match_ids: set) -> list:
        # All the cddb entry ids
        cddb_entry_ids = {entry["id"] for entry in cddb_entries}
        # All the ids which are in a match
        all_ids_in_match = {id for match_id_pair in match_ids for id in match_id_pair}

        # All the ids which are not in a match
        not_duplicate_ids = cddb_entry_ids - all_ids_in_match 

        # All the entries which are not in a match
        not_duplicates = [entry for entry in cddb_entries if entry["id"] in not_duplicate_ids]

        # Add all these entries to the merged entries
        merged_entries.extend(not_duplicates)
        return merged_entries
 
    def merge_matches(self, cddb_entries: list, matches_path: str, similarity_mode: dict) -> list:
        # Load matches from the matches CSV
        match_ids = self._load_matches(matches_path)
        # Create groups to be merged with networkx library
        merge_groups = self._get_merge_groups(match_ids)
        # Merge entries in the groups using the merge strategies
        merged_entries = self._merge_entries_in_groups(merge_groups, cddb_entries, similarity_mode)
        # Add the entries from the original entries which were included as dublicates before
        merged_entries = self._add_not_duplicates(merged_entries, cddb_entries, match_ids)
        return merged_entries

    def _create_dom(self, merged_entries: list) -> Document:
        # Create a new DOM document
        doc = Document()
        
        # Create root element (discs)
        root = doc.createElement('discs')
        doc.appendChild(root)
        
        # Create new disc elements for each merged entry
        for entry in merged_entries:
            disc_element = doc.createElement('disc')
            
            # Add simple elements (id, cid, artist, dtitle, category)
            for key in ['id', 'cid', 'artist', 'dtitle', 'category']:
                if key in entry:
                    element = doc.createElement(key)
                    value = entry[key]
                    if isinstance(value, list):
                        value = ','.join(str(v) for v in value)
        
                    text = doc.createTextNode(str(value))
                    element.appendChild(text)
                    disc_element.appendChild(element)
            
            # Add tracks element with title subelements
            if 'tracks' in entry:
                tracks_element = doc.createElement('tracks')
                for track in entry['tracks']:
                    title_element = doc.createElement('title')
                    text = doc.createTextNode(track)
                    title_element.appendChild(text)
                    tracks_element.appendChild(title_element)
                disc_element.appendChild(tracks_element)

            root.appendChild(disc_element)
        
        return doc
    
    def _save_merges(self, dom: Document, filepath: str, mode_name: str, with_timestamp=False, timestamp_value=None) -> None:
        filepath = filepath + f"_{mode_name}"
        save_to_xml(filepath, dom, with_timestamp=with_timestamp, timestamp_value=timestamp_value, pretty_xml=True)

    def create_and_save_merges_with_all_modes(self, cddb_entries: list, matches_path: str, new_disk_xml_path: str, with_timestamp=False, timestamp_value=None) -> None:
        for mode_name in self.similarity_modes:
            mode = self.similarity_modes[mode_name]
            merged_entries = self.merge_matches(cddb_entries, matches_path, similarity_mode=mode)
            merged_entries_dom = self._create_dom(merged_entries)
            self._save_merges(merged_entries_dom, new_disk_xml_path, mode_name=mode_name, with_timestamp=with_timestamp, timestamp_value=timestamp_value)

