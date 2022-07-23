import pymysql 
import yaml
import os
import sys
PROJ_ROOT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(PROJ_ROOT_PATH)

try:
    
    from common.IsServiceAlive import Server
except ImportError as err:
    print(err)
    
'''
@author JunHyeon.Kim
@date 20220723
'''
class MySQLClient:
    
    _FLAG_ = "MYSQL" 
    def __init__(self) -> None:
        self.mysqlClient = MySQLClient.getMySQLClient()
    
    @classmethod 
    def getMySQLClient(cls):
        '''
        :param:
        :return:
        '''
        global PROJ_ROOT_PATH
        mysqlConfig = os.path.join(PROJ_ROOT_PATH, "config/mysqlConn.yml")
        isExists = os.path.exists(mysqlConfig) 
        
        if isExists:
            isFile = os.path.isfile(mysqlConfig)
            if isFile:
                with open(mysqlConfig, "r", encoding="utf-8") as mysqlConn:
                    connConfig = yaml.safe_load(mysqlConn)
                    mysqlConn.close()
                    
                    isAlive = Server.isServiceAlive(
                        config= connConfig 
                        ,category_key= MySQLClient._FLAG_
                    )
                    if isAlive:
                        MYSQL = connConfig[MySQLClient._FLAG_]
                        conn = pymysql.connect(
                            host= MYSQL["host"], 
                            user= MYSQL["user"], 
                            password= MYSQL["password"], 
                            charset="utf-8")
                        
                        return conn
                    else:
                        print("mysql service 가 close 되어 있는것 같아")
                        
                    
        else:
            raise FileNotFoundError 