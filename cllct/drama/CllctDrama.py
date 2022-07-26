import os
import sys
from datetime import datetime

PROJ_ROOT_PATH = os.path.abspath(os.path.dirname(__file__)) 
for _ in range(2):
    PROJ_ROOT_PATH = os.path.dirname(PROJ_ROOT_PATH)

sys.path.append(PROJ_ROOT_PATH)

from bs4 import BeautifulSoup
import json
import base64

try:
    
    from model.drama.ModelDrama import ModelDrama 
    from common.CommonUrl import CommonUrl
    from common.Category import Category
    from common.ElementTemplate import ElementTemplate
    from common.EsComm import EsCommon
    from client.SeleniumClient import SeleniumClient
    from util.TimeUtil import TimeUtil
    from es.Client import EsClient
    from es.EsService import EsService
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
    
    def hitDocumentDelete(self, paramDate):
        '''
        :param:
        :return:
        '''
        query = EsService.rmDocument(paramDate= paramDate)
        try:
            
            self.esClient.delete_by_query(body=query, index="es_time_range") 
        except:
            print(f"[{paramDate}] date delete fail !!")
        else:
            print(f"[{paramDate}] date delete success !!")
        
    def getEsCllctTime(self):
        '''
        :param:
        :return:
        '''
        query = EsService.getDateQuery()
        response = self.esClient.search(body=query, index="es_time_range")
        date_col= dict(
            json.loads(
                json.dumps(
                    response, ensure_ascii=False, indent=3, sort_keys=True
                )
            )
        )  
         
        date = date_col["hits"]["hits"][0]["_source"]["date_col"]
        date_time_obj = datetime.strptime(date, '%Y%m%d')
        date_time_obj = str(date_time_obj).split(" ")[0].replace("-", "")
        return date_time_obj 
         
    def insertMySQL(self, totalCount: int):
        '''
        :param:
        :return:
        '''
        print(f"** Elasticsearch insert totalCount : {totalCount}")        
    
    def getData(self):
        '''
        :param:
        :return:
        '''
        totalCount = 0
        cllct = self.getEsCllctTime()
        
        # Year ----    
        reqUrl = self.baseUrl + "?" + self.urlParam + "&date=" + cllct 
        
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
                    try:
                        
                        e["mv_access_url"] = "https://movie.naver.com" + aTag.attrs["href"]
                        e["mv_ranking"] = movieRanking
                        e["mv_title"] = aTag.attrs["title"] 
                        e["mv_category"] = self.category 
                        e["cllct_time"] = self.cllctTime
                    except AttributeError as err:
                        print(err)
                    else:
                        encodedBytes = base64.b64encode(e['mv_title'].encode('utf-8'))
                        encodedStrTitle = str(encodedBytes, "utf-8")
                        
                        docId = "movieCategory({category})_movieTitle({title})".format(
                            category = e['mv_category'], 
                            title = encodedStrTitle 
                        )
                        
                        self.action.append(
                            {
                                "_index": self.index
                                ,"_id": docId
                                ,"_source": {
                                    **e,
                                    "insert_time": cllct
                                }
                            }
                        )
                    finally:
                        # row count increase
                        totalCount = totalCount + 1
                    
            # Elastifcsearch 에 데이터 적재
            self.dataBulkInsert()
            
            # action list 데이터 empty  
            self.action.clear()
        chromeClient.close()
        # getData function end =======================
        self.insertMySQL(totalCount= totalCount)
        self.hitDocumentDelete(paramDate=cllct)

if __name__ == "__main__":

    print(f"** PROJ_ROOT_PATH: {PROJ_ROOT_PATH}")
    o = CllctDrama()
    o.getData()
