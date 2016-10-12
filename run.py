import os
import runpy

from time import sleep
from daemonize import Daemonize

import argparse

parser = argparse.ArgumentParser(description='freewifi gateway daemon')
parser.add_argument('--pidfile', help='file to write pid to')
args = parser.parse_args()

def main():
    while True:
        rootpath = os.path.abspath(os.path.dirname(__file__))
        os.sys.path.append(rootpath)
        ret = runpy.run_module('freewifi_gateway')
        print('ret', ret)
        sleep(20)
        
daemon = Daemonize(app="freewifi_gateway", pid=args.pidfile, action=main)
daemon.start()
