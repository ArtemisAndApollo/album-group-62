from handlers.cbbd_handler import CbbdHandler

class GroundTruthHandler(CbbdHandler):
    def __init__(self, total_pairs: int = 0):
        super().__init__(total_items=total_pairs, handle_type="pair")

    def _analyze_end_element(self, name: str):
        self._select_default(name)
        if name == "disc":
            self.id_list.append(self.id)
            self.cid_list.append(self.cid)
        elif name == "pair":
            self.entry_list.append(
                {
                    "id_0": self.id_list[0],
                    "cid_0": self.cid_list[0],
                    "id_1": self.id_list[1],
                    "cid_1": self.cid_list[1]
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
    
            
