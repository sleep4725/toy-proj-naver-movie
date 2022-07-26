from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.helpers import errors

import yaml 
import os
import sys
PROJ_ROOT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(PROJ_ROOT_PATH)

try:
    from customexc.ExceptionSeviseClose import ExceptionServiceClose
    from common.IsServiceAlive import Server
except ImportError as err:
    print(err)
##
# @author JunHyeon.Kim
# @date 20220723
## --------------------------
class EsClient:
    
    _FLAG_ = "ES"
      
    def __init__(self) -> None:
        self.esClient = EsClient.getEsClient() 
        self.action = list()
    
    def dataBulkInsert(self):
        '''
        :param:
        :return:
        '''
        print(f"self.action.size : {len(self.action)}")
        if len(self.action) != 0: 
            try:
                
                bulk(self.esClient, actions= self.action)
            except errors.BulkIndexError as err:
                print(err)
            else:
                print("bulk insert success")   
        else:
            print("적재할 수 있는 데이터가 없습니다.")
                
    @classmethod 
    def getEsClient(cls)-> Elasticsearch:
        '''
        :param:
        :return Elasticsearch-Client:
        '''
        global PROJ_ROOT_PATH 
        esConfigFile = os.path.join(PROJ_ROOT_PATH, "config/esConn.yml")
        
        #
        isExists = os.path.exists(esConfigFile)       
        if isExists:
            isFile = os.path.isfile(esConfigFile)       
            if isFile:
                with open(esConfigFile, "r", encoding="utf-8") as es:
                    esConfig = yaml.safe_load(es)
                    es.close()
                    
                    isAlive = Server.isServiceAlive(
                        config= esConfig
                        ,category_key= EsClient._FLAG_
                    )
                    if isAlive:
                        ES = esConfig[EsClient._FLAG_] 
                        esHosts = [f"{ES['http']}://{e}:{ES['port']}" for e in ES["host"]]
                        print(f"**esHosts => {esHosts}") 
                        
                        try:
                        
                            esClient = Elasticsearch(esHosts)
                        except:
                            print(f"error~")
                        else:    
                            response = esClient.cluster.health()
                            if response["status"] in ["yellow", "green"]:
                                return esClient
                            else:
                                return None
                    else:
                        print("node가 죽어있는것 같아") 
                        raise ExceptionServiceClose                      
        else:
            raise FileNotFoundError
