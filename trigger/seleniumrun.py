import shlex
import subprocess 

def runSeleniumProcess():
    '''
    '''
    global runQueryList
    subprocess.run(runQueryList, stdout=subprocess.PIPE)

if __name__ == "__main__":
    runQuery = '''/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="./sampleChromeProfile"'''
    runQueryList = shlex.split(runQuery)
    
    print(f"** {runQueryList}")
    runSeleniumProcess()