from handlers.cbbd_handler import CbbdHandler
import re

class DiscHandler(CbbdHandler):
    def __init__(self, total_discs: int = 0, sanitization_features: dict = None):
        super().__init__(total_items=total_discs, handle_type="disc", sanitization_features=sanitization_features)       
    
    def _analyze_end_element(self, name: str):
        self._select_default(name)
        if name == "artist":
            artist_name = "".join(self.string_builder).strip()
            if self.san_feat is not None: 
                if "swap_name_with_extra_info" in self.san_feat and self.san_feat["swap_name_with_extra_info"]:
                    artist_name = self._swap_name_with_extra_info(artist_name)
                if "strip_apostroph" in self.san_feat and self.san_feat["strip_apostroph"] and (artist_name.startswith("'") or artist_name.endswith("'")):
                    artist_name = artist_name.strip("'")
            self.artist = self._remove_corrupted_unicode(artist_name)
        elif name == "dtitle":
            self.dtitle = self._remove_corrupted_unicode("".join(self.string_builder).strip())
        elif name == "category":
            self.category = "".join(self.string_builder).strip()
        elif name == "title":
            track_title = "".join(self.string_builder).strip()
            if self.san_feat is not None:
                if "replace_degree_sign" in self.san_feat and self.san_feat["replace_degree_sign"] and "°" in track_title:
                    track_title = track_title.replace("°", "degrees")
                if "remove_time_in_tracks" in self.san_feat and self.san_feat["remove_time_in_tracks"] and re.search(r"^\d\.\d\d\s[AM]{2}\s", track_title):
                    track_title = re.sub(r"^\d\.\d\d\s[AM]{2}\s", "", track_title).lstrip("(").rstrip(")")
                if "remove_track_numbers" in self.san_feat and self.san_feat["remove_track_numbers"]:
                    if re.search(r"^\d{1,2}[-\s\.]+\S", track_title) and not re.search(r"^\d{1,2}\s(Degrees)", track_title, flags=re.IGNORECASE): # find "01. title"/"1. title"/"01-title"/"1-title"/"01 - title"/"1 - title" with possibly a letter directly after it.
                        track_title = re.sub(r"^\d{1,2}[-\s\.]+", "", track_title).strip()
                    elif re.search(r"\D\/\s*\d{1,2}[\s\-]+", track_title): # find "artist name / 01 - "
                        track_title = re.sub(r"\\D\/\s*\d{1,2}[\s\-]+", "/ ", track_title).strip()
                if "remove_artist_name_in_tracks" in self.san_feat and self.san_feat["remove_artist_name_in_tracks"]:
                    escaped_artist = re.escape(self.artist)
                    track_title = re.sub(rf"^{escaped_artist}\s*\/\s*", "", track_title, flags=re.IGNORECASE).strip()
                if "replace_number_to_apostrophe" in self.san_feat and self.san_feat["replace_number_to_apostrophe"] and re.search(r"[A-Za-z]\d[A-Za-z]", track_title):
                    track_title = re.sub(r"([A-Za-z])\d([A-Za-z])", r"\1'\2", track_title)
            
            self.tracks_list.append(self._remove_corrupted_unicode(track_title))
        elif name == "disc":
            self.entry_list.append(
                {
                    "id": self.id,
                    "cid": self.cid.split(";"),
                    "artist": self.artist,
                    "dtitle": self.dtitle,
                    "category": self.category,
                    "tracks": self.tracks_list,
                }
            )

    def _init_and_reset_specific_variables(self):
        self.id = ""
        self.cid = ""

        self.artist = ""
        self.dtitle = ""
        self.category = ""
        self.title = ""
        self.tracks_list = []

    def _remove_corrupted_unicode(self, text: str):
        if "remove_corrupted_unicode" in self.san_feat and self.san_feat["remove_corrupted_unicode"] and "�?" in text:
            text = text.replace("�?", "")
        return text