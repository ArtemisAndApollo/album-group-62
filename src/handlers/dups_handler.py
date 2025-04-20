from handlers.cbbd_handler import CbbdHandler

class DupsHandler(CbbdHandler):
    def __init__(self, total_pairs: int = 0, sanitization_features: dict = None):
        super().__init__(total_items=total_pairs, handle_type="pair", sanitization_features=sanitization_features)

    def _analyze_end_element(self, name: str):
        self._select_default(name)
        if name == "artist":
            self.artist = "".join(self.string_builder).strip()
        elif name == "dtitle":
            self.dtitle = "".join(self.string_builder).strip()
        elif name == "category":
            self.category = "".join(self.string_builder).strip()
        elif name == "title":
            self.disc_tracks_list.append("".join(self.string_builder).strip())
        elif name == "disc":
            self.id_list.append(self.id)
            self.cid_list.append(self.cid)
            self.artist_list.append(self.artist)
            self.dtitle_list.append(self.dtitle)
            self.category_list.append(self.category)
            self.tracks_list.append(self.disc_tracks_list)
            self.disc_tracks_list = []
        elif name == "pair":
            self.entry_list.append(
                {
                    "id_0": self.id_list[0],
                    "cid_0": self.cid_list[0].split(";"),
                    "artist_0": self.artist_list[0],
                    "dtitle_0": self.dtitle_list[0],
                    "category_0": self.category_list[0],
                    "tracks_0": self.tracks_list[0],
                    "id_1": self.id_list[1],
                    "cid_1": self.cid_list[1].split(";"), 
                    "artist_1": self.artist_list[1],
                    "dtitle_1": self.dtitle_list[1],
                    "category_1": self.category_list[1],
                    "tracks_1": self.tracks_list[1],
                }
            )
    
    def _init_and_reset_specific_variables(self):
        self.id = ""
        self.cid = ""
        self.id_list = []
        self.cid_list = []

        self.artist = ""
        self.dtitle = ""
        self.category = ""
        self.title = ""
        self.artist_list = []
        self.dtitle_list = []
        self.category_list = []
        self.tracks_list = []
        self.disc_tracks_list = []      
