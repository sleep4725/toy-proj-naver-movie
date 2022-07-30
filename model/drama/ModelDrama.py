from urllib.parse import urlencode

'''
네이버 영화 (드라마)
@author JunHyeon.Kim
@date 20220730
'''
class ModelDrama:
    
    TG = 1 
    
    def __init__(self) -> None:
        self.urlParam = urlencode({
            "sel": "cnt",
            "tg": ModelDrama.TG 
        })