import socket
import subprocess
from urllib import response

'''
@author JunHyeon.Kim
@date 20220723
'''
class Server:
    
    @classmethod
    def isServiceAlive(cls, config, category_key)-> bool:
        '''
        :param:
        :return:
        ''' 
        isAliveCheck = True
        port = config[category_key]["port"] 
        respCode, _ = subprocess.getstatusoutput(f"lsof -n -i :{port} | grep LISTEN")

        if not respCode:
            return isAliveCheck
        else:
            isAliveCheck = False
            return isAliveCheck
        
    @classmethod
    def isServiceAliveOldVersion(cls, config, category_key)-> bool:
        '''
        :param config:
        :param k:
        :param servicePort:
        :param category:
        :return:
        '''
        isAliveCheck = True
        port = config[category_key]["port"]
        for host in config[category_key]["host"]:
            print(f"{category_key} service alive check host: {host} | port: {port}")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
            if sock.connect_ex((host, port)) == 0:
                print("Port is open~!!")
            else:
                print("Port is not open")
                isAliveCheck = False
                break
        
        return isAliveCheck