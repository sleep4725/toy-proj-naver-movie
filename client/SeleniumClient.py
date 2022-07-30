import shlex
import os
import subprocess
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

'''
@author JunHyeon.KIm
@date 20220723
'''
class SeleniumClient:
   
   @classmethod
   def getChromeObject(cls)-> webdriver.Chrome:
       
       '''
       :param:
       :return:
       '''
       homePath = os.path.expanduser("~")
       _port = 9222
       _user_data_dir = f"{homePath}/sampleChromeProfile" 

       runQuery = f'''/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome 
        --remote-debugging-port={_port} 
        --user-data-dir="{_user_data_dir}"'''
       runQueryList = shlex.split(runQuery)
       subprocess.run(runQueryList, stdout=subprocess.PIPE)
       
       op = Options()
       op.add_experimental_option('debuggerAddress', "127.0.0.1:9222")
       chrome_driver = webdriver.Chrome(options=op)
       return chrome_driver    
    