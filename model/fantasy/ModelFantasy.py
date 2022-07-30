from urllib.parse import urlencode

'''
네이버 영화 (판타지)
@author JunHyeon.Kim
@date 20220730
'''
class ModelFantasy:
    
    TG = 2 
    
    def __init__(self) -> None:
        self.urlParam = urlencode({
            "sel": "cnt",
            "tg": ModelFantasy.TG 
        })