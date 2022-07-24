'''
@author JunHyeon.Kim
@date 20220723
'''
class ExceptionServiceClose(Exception):
    
    def __init__(self) -> None:
        super().__init__("service close")
    