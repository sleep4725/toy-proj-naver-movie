from urllib.parse import urlencode

class ModelDrama:
    
    TG = 2 
    
    def __init__(self) -> None:
        self.urlParam = urlencode({
            "sel": "cnt",
            "tg": ModelDrama.TG 
        })