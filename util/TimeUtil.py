import time 

'''
@author JunHyeon.Kim
@date 20220723
''' 
class TimeUtil:
    
    @classmethod
    def getCllctTime(cls):
        '''
        :param:
        :return:
        '''
        cllctTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"** cllctTime : {cllctTime}")
        
        return cllctTime