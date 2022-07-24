import pandas as pd
from datetime import datetime
import os
import sys
PROJ_ROOT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(PROJ_ROOT_PATH)

from es.Client import EsClient
'''
@author JunHyeonKim
@date 20220723
'''
class TimeSetup(EsClient):
    
    def __init__(self) -> None:
        EsClient.__init__(self)
        self.es_index = "es_time_range"

    def getTimeRange(self):
        '''
        :param:
        :return:
        '''
        timeRange = pd.date_range(start='1/1/2018', periods=36, freq='M')
                
        for t in timeRange:
            self.action.append({
                "_index": self.es_index 
                ,"_id": str(t).split(" ")[0].replace("-", "")
                ,"_type": "daterange"
                ,"_source": {
                    "date_col": str(t).split(" ")[0].replace("-", "")
                }
            }) 
        
        self.dataBulkInsert()
            
if __name__ == "__main__":
    o = TimeSetup()
    o.getTimeRange()
    