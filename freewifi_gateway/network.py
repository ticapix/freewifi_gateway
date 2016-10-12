import os
import subprocess

def call(*cmd):
    print('exec', ' '.join(cmd))
    return subprocess.check_output(cmd)

def init_interfaces():
    # by default, select the 1st available PHY device
    phy_name = os.listdir('/sys/class/ieee80211')[0]
    phy_mac = open(os.path.join('/sys/class/ieee80211', phy_name, 'macaddress'), 'r').readline().strip('\n\r')
    print("physical interface", phy_name, "(", phy_mac, ")")
    
    # delete existing interfaces
    for iface in os.listdir(os.path.join('/sys/class/ieee80211', phy_name, 'device/net')):
        call('iw', 'dev', iface, 'del')

    # create two new interfaces
    # with non-conventional name to avoid conflicts with some network auto conf leftover
    call('iw', 'phy', phy_name, 'interface', 'add', 'wlan0_ap', 'type', 'managed') # ap
    call('iw', 'phy', phy_name, 'interface', 'add', 'wlan0_sta', 'type', 'managed') # station
    
    # bringing down the interfaces before changing the mac addresses
    call('ip', 'link', 'set', 'dev', 'wlan0_ap', 'down')
    call('ip', 'link', 'set', 'dev', 'wlan0_sta', 'down')

    # changing the mac addresses
    call('ip', 'link', 'set', 'dev', 'wlan0_ap', 'address', phy_mac[:-1] + '0')
    call('ip', 'link', 'set', 'dev', 'wlan0_sta', 'address', phy_mac[:-1] + '1')
    
    # bring up the interface
    call('ip', 'link', 'set', 'dev', 'wlan0_ap', 'up')
    call('ip', 'link', 'set', 'dev', 'wlan0_sta', 'up')

def is_FreeWifi_available():
    for line in call('iw', 'dev', 'wlan0_ap', 'scan').decode('utf-8').split('\n'):
        if "SSID: FreeWifi" in line:
            return True
    return False


def connect_FreeWifi():
    """network={
          ssid="FreeWifi"
          key_mgmt=NONE
        }
    """
    call('wpa_supplicant', '-Dnl80211', '-iwlan0_sta', '-c/tmp/wpa_supplicant.conf')

#     curl -X POST -F 'login=3087856586' -F 'password=ticapix57'  https://wifi.free.fr/Auth

#     curl -X POST -F 'login=3087856586' -F 'password=ticapix57' 'https://wifi.free.fr/Auth?url=http://www.bing.com/'
     
