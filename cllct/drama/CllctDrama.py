import os
import sys
from unicodedata import category
PROJ_ROOT_PATH = os.path.abspath(os.path.dirname(__file__)) 
for _ in range(2):
    PROJ_ROOT_PATH = os.path.dirname(PROJ_ROOT_PATH)

sys.path.append(PROJ_ROOT_PATH)

from bs4 import BeautifulSoup

try:
    
    from model.drama.ModelDrama import ModelDrama 
    from common.CommonUrl import CommonUrl
    from common.Category import Category
    from common.ElementTemplate import ElementTemplate
    from common.EsComm import EsCommon
    from client.SeleniumClient import SeleniumClient
    from util.TimeUtil import TimeUtil
    from es.Client import EsClient
    from db.MySQLClient import MySQLClient
except ImportError as err:
    print(err)

'''
@author JunHyeon.Kim
@date 20220723
'''
class CllctDrama(ModelDrama, EsClient, EsCommon, MySQLClient):

    def __init__(self) -> None:
        ModelDrama.__init__(self)
        EsCommon.__init__(self)
        EsClient.__init__(self) # Elasticsearch Client model setting
        MySQLClient.__init__(self)
        
        self.baseUrl = CommonUrl.getBaseUrl()
        self.cllctTime = TimeUtil.getCllctTime()
        self.category = Category.getCategoryInformation(ModelDrama.TG) 
    
    def insertMySQL(self, totalCount: int):
        '''
        :param:
        :return:
        '''
        print(f"** Elasticsearch insert totalCount : {totalCount}")        
    
    def getData(self):
        '''
        :param:
        :return:ß
        '''
        totalCount = 0
        # Year ----    
        reqUrl = self.baseUrl + "?" + self.urlParam + "&date=20220721"
        
        print(f"** reqUrl: {reqUrl}")
        chromeClient = SeleniumClient.getChromeObject()
        
        chromeClient.get(reqUrl)
        chromeClient.implicitly_wait(3)
        bsObject = BeautifulSoup(chromeClient.page_source, "html.parser")
             
        listRanking = bsObject.select_one("table.list_ranking")
        trList = listRanking.select_one("tbody").select("tr")

        if len(trList) != 0:
            flagCount = 0
            movieRanking = 0
            
            for element in trList[1:]:
                flagCount = flagCount + 1
                if flagCount == 11:
                    flagCount = 0
                else:
                    movieRanking = movieRanking + 1
                    aTag = element.select_one("td.title > div.tit3 > a")
                    e = ElementTemplate.getTemplate()
                    e["mv_access_url"] = aTag.attrs["href"]
                    e["mv_ranking"] = movieRanking
                    e["mv_title"] = aTag.attrs["title"] 
                    e["mv_category"] = self.category 
                    e["cllct_time"] = self.cllctTime
                    print(e)
                    self.action.append(
                        {
                            "_index": self.index
                            ,"_type": self.category
                            ,"_source": e
                        }
                    )
                    # row count increase
                    totalCount = totalCount + 1
                    
            # Elastifcsearch 에 데이터 적재
            self.dataBulkInsert()
            
            # action list 데이터 empty  
            self.action.clear()
        chromeClient.close()
        # getData function end =======================
        self.insertMySQL(totalCount= totalCount)
        
if __name__ == "__main__":
    print(f"** PROJ_ROOT_PATH: {PROJ_ROOT_PATH}")
    o = CllctDrama()
    o.getData()