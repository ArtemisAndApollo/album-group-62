from xml.sax.handler import ContentHandler

class CbbdHandler(ContentHandler):
    def __init__(self, handle_type, total_items, sanitization_features: dict = None):
        self.tag = None
        self.string_builder = []
        self.string_list = []
        self.entry_list = []
        self.item_key = 0
        self.total_items = total_items
        if handle_type is None:
            raise Exception("Handle_type is not provided")
        self.handle_type = handle_type
        self.san_feat = sanitization_features

        self._init_and_reset_specific_variables()

    def startElement(self, name: str, attrs):
        self.tag = name
        if self.tag == self.handle_type:
            self.item_key += 1

    def endElement(self, name: str):
        self.tag = None
        if name == self.handle_type and self.item_key>self.total_items:
            raise Exception("")
        
        self._analyze_end_element(name)

        if name == self.handle_type:
            self._init_and_reset_specific_variables()

        self.string_builder = []

    def characters(self, content: str):
        if content.strip() != "" and self.tag is not None:
            if self.san_feat is not None:
                if "replace_amp" in self.san_feat and self.san_feat["replace_amp"] and "&" in content:
                    content = content.replace("&", "and")
                if "replace_incorrect_apostroph" in self.san_feat and self.san_feat["replace_incorrect_apostroph"] and "´" in content:
                    content = content.replace("´", "'")
            self.string_builder.append(content)

    def _select_default(self, name: str):
        if name == "id":
            self.id = "".join(self.string_builder).strip()
        elif name == "cid":
            self.cid = "".join(self.string_builder).strip().replace(",", ";")

    def _init_and_reset_specific_variables(self):
        pass

    def _analyze_end_element(self, name: str):
        pass

    def _swap_name_with_extra_info(self, name: str):
        if "," in name:
            if "(" in name:
                artist_name, extra_info = name.split("(", 1)
                return self._swap_name(artist_name) + " (" + extra_info
            else:
                return self._swap_name(name)
        else:
            return name.strip()
            
    def _swap_name(self, name: str):
        last_name, first_name = name.split(",", 1)
        return first_name.strip() + " " + last_name.strip()

        

