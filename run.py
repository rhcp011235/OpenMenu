# This is the main script that you will run all the others with
# 

import os
import subprocess
import multiprocessing
import time
import sys

scriptFolder = os.path.dirname(os.path.abspath(__file__))
os.chdir(scriptFolder)

# You made need to modify the path to mitmweb here
mitmweb_command = 'mitmweb -s proxy.py --set block_global=false --set web_open_browser=false --allow-hosts "profile\.gc\.apple\.com|.*-fmfmobile\.icloud\.com"'
proxyapi_command = 'python3 proxyapi.py'  

def run_mitmweb():
    mitmweb_process = subprocess.Popen(mitmweb_command, shell=True)
    mitmweb_process.wait()


def run_proxyapi():
    proxyapi_process = subprocess.Popen(proxyapi_command, shell=True)
    proxyapi_process.wait()

if __name__ == '__main__':
    mitmweb_process = multiprocessing.Process(target=run_mitmweb)
    proxyapi_process = multiprocessing.Process(target=run_proxyapi)
    proxyapi_process.start()
    mitmweb_process.start()
    while True:
        time.sleep(1)
        if not mitmweb_process.is_alive() or not proxyapi_process.is_alive():
            # If one process exits, terminate the other
            if mitmweb_process.is_alive():
                mitmweb_process.terminate()
            if proxyapi_process.is_alive():
                proxyapi_process.terminate()
            sys.exit(0)