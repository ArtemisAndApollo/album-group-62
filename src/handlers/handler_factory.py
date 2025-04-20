from handlers.disc_handler import DiscHandler
from handlers.dups_handler import DupsHandler
from handlers.ground_truth_handler import GroundTruthHandler
from xml.sax import parse

class HandlerFactory():
    def __init__(self):
        self.handlers = {
            "disc": DiscHandler,
            "dups": DupsHandler,
            "ground-truth": GroundTruthHandler
        }

    def create(self, handler_type: str, total_items: int = 0, data_path: str = "", sanitization_features: dict = None):
        if handler_type not in self.handlers:
            raise ValueError("Invalid handler type")
        
        handler = self.handlers[handler_type]
        return self.BaseHandler(handler, total_items, data_path, sanitization_features)
        

    class BaseHandler():
        def __init__(self, handler, total_items, data_path, sanitization_features):
            self.handler = handler(total_items, sanitization_features)

            try:
                parse(data_path, self.handler)
            except Exception as e:
                print(e)
    
        def get_entries(self) -> list:
            return self.handler.entry_list