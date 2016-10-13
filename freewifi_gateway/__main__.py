import sys

try:
    import jinja2
    import flask
except ImportError as e:
    print(e)
    print("this script must run from the virtual environment")
    sys.exit(1)


from . import network

network.init_interfaces()

print(network.is_FreeWifi_available())

import time
while True:
    time.sleep(1)
    
sys.exit(0)

class State(object):
    def __init__(self, statemachine):
        self.statemachine = statemachine

        
class SearchFreeWifi(State):
    def run(self):
        if network.is_FreeWifi_available():
            return State.FreeWifi_Found
        return State.FreeWifi_NotFound

    def next(self, input):
        if input == State.FreeWifi_Found:
            return Action.Connect_FreeWifi
        return Action.CreateAP_NoConstrain

class ConnectFreewifi(State):
    def run(self):
        # shutdown hostapd+dnsmasq+ip confs
        # connect wifi
        # dhclient wlan0_sta
        pass

    def next(self, input):
        return Action.Share_Internet_LAN
        return Action.CreateAP_Constrained

class CreateAPNoConstrain(State):
    def run(self):
        # configure interface wlan0_ap with IP
        # dnsmasq
        # hostapd
        pass

    def next(self, input):
        return Action.Search_FreeWifi

class CreateAPConstrained(State):
    def run(self):
        # get freewifi channel
        # configure interface wlan_ap with IP
        # dnsmasq
        # hostapd
        pass

    def next(self, input):
        return Action.Check_Connection

class CheckConnection(State):
    def run(self):
        # check default route via wlan_sta
        # check access 8.8.8.8
        if ok:
            return State.Connected
        return State.Disconnected
    
    def next(self, input):
        if input == State.Connected:
            return Action.Check_Connection
        return Action.Search_FreeWifi
        
sys.exit(0)
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
