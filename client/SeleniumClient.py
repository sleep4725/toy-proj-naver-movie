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
       op = Options()
       op.add_experimental_option('debuggerAddress', "127.0.0.1:9222")
       chrome_driver = webdriver.Chrome(options=op)
       chrome_driver.get("https://www.naver.com/")
       return chrome_driver    
    