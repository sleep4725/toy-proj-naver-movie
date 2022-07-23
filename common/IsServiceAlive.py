import socket

'''
@author JunHyeon.Kim
@date 20220723
'''
class Server:
    
    @classmethod
    def isServiceAlive(cls, config, category_key)-> bool:
        '''
        :param config:
        :param k:
        :param servicePort:
        :param category:
        :return:
        '''
        isGood = True
        port = config[category_key]["port"]
        for host in config[category_key]["host"]:
            s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((host, port))
            
            if result == 0:
                print(f"{category_key} service open~")
            else:
                isGood = False
                print(f"{category_key} service close~") 
                
        return isGood