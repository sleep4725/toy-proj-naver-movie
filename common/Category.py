'''
@author JunHyeon.Kim
@date 20220730
'''
class Category:
    
    @classmethod
    def getCategoryInformation(cls, checkNum):
        '''
        :param checkNum:
        '''
        information = {
            1: "drama"
            ,2: "fantasy"
        } 
        
        if checkNum in information.keys():
            return information[checkNum]
        else:
            return "null"
        
        