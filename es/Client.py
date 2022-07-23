from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import yaml 
import os
import sys
PROJ_ROOT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(PROJ_ROOT_PATH)

try:
    
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
        '''
            
        bulk(self.esClient, actions= self.action)
    
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
        else:
            raise FileNotFoundError
