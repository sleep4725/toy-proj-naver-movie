import subprocess

respCode, _ = subprocess.getstatusoutput("lsof -n -i :3306 | grep LISTEN")
print(respCode)