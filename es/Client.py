from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import yaml 
import socket
import os
PROJ_ROOT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

##
# @author JunHyeon.Kim
# @date 20220723
## --------------------------
class EsClient:
    
    def __init__(self) -> None:
        self.esClient = EsClient.getEsClient() 
        self.action = list()
    
    def dataBulkInsert(self):
        '''
        '''
            
        bulk(self.esClient, actions= self.action)
    
    @classmethod
    def isServiceAlive(cls, esConfig)-> bool:
        '''
        :param:
        :return:
        '''
        isGood = True 
        for host in esConfig["esHosts"]:
            print(host)
            s = socket.socket()
        
            try:
                
                s.connect((host, esConfig["esPort"]))
            except ConnectionRefusedError as err:
                print(err)
                isGood = False   
                break
            
        
        return isGood 
         
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
                    if EsClient.isServiceAlive(esConfig=esConfig):
                        '''http://'''
                        esHosts = [f"{esConfig['esHttp']}://{e}:{esConfig['esPort']}" for e in esConfig["esHosts"]]
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
