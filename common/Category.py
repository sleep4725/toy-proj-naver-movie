'''
@author JunHyeon.Kim
'''
class Category:
    
    @classmethod
    def getCategoryInformation(cls, checkNum):
        '''
        '''
        information = {
            2: "drama"
        } 
        
        if checkNum in information.keys():
            return information[checkNum]
        else:
            return "null"