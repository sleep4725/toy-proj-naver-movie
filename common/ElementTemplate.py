'''
@author JunHyeon.Kim
@date 20220723
'''
class ElementTemplate:
    
    @classmethod
    def getTemplate(cls):
        '''
        :param:
        :return:
        '''
        e = {
            "mv_access_url": ""
            ,"mv_ranking": 0
            ,"mv_title": ""
            ,"mv_category": ""
            ,"cllct_time": "1900 01 01 00:00:00"
        }
        
        return e