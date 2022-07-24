import subprocess

command = "/usr/sbin/lsof -n -i :3123122 | grep LISTEN"

#subprocess.run(command, shell=True, check=True)
subprocess.(command, shell=True, check=True)