from multiprocessing import Process
import subprocess
from .tools import run
from string import Template

hostapd_conf_filename = "/tmp/freewifi_hostapd.conf"

hostapd_defaults = {
    'SSID': 'mywifi',
    'WPA_PASS': 'myfreewifi',
    'CHANNEL': 4,
    'BROADCAST': 0
}


hostapd_conf = Template("""
ssid=$SSID
interface=wlan0_ap
driver=nl80211
country_code=FR
channel=$CHANNEL

# a = IEEE 802.11a, b = IEEE 802.11b, g = IEEE 802.11g
hw_mode=g

wpa=2
wpa_passphrase=$WPA_PASS

# Key management algorithms ##
wpa_key_mgmt=WPA-PSK

# Set cipher suites (encryption algorithms) ##
# TKIP = Temporal Key Integrity Protocol
# CCMP = AES in Counter mode with CBC-MAC
wpa_pairwise=TKIP
rsn_pairwise=CCMP

# Shared Key Authentication ##
auth_algs=1

# Accept all MAC address ###
macaddr_acl=0

#setting ignore_broadcast_ssid to 1 will disable the broadcasting of ssid
ignore_broadcast_ssid=$BROADCAST
""")


class Service(object):
    def __init__(self):
        self._hostapd = None
        self._dnsmasq = None
        
    def restart(self, **kwargs):
        run('ip', 'addr', 'add', '10.0.0.1/24', 'dev', 'wlan0_ap')
        
        options = hostapd_defaults.copy()
        options.update(kwargs)
        self.stop()
        with open(hostapd_conf_filename, 'w') as fd:
            fd.write(hostapd_conf.substitute(options))
        cmd = ['hostapd', hostapd_conf_filename]
        self._hostapd = Process(target=subprocess.call, args=(cmd,)).start()

        cmd = ['dnsmasq', '--keep-in-foreground', '--interface=wlan0_ap', '--bind-interfaces', '--dhcp-range=10.0.0.10,10.0.0.254,12h']
        self._dnsmasq = Process(target=subprocess.call, args=(cmd,)).start()
        
    def stop(self):
        if self._hostapd is not None:
            self._hostapd.terminate()
            self._hostapd.join(30)
        if self._dnsmasq is not None:
            self._dnsmasq.terminate()
            self._dnsmasq.join(30)
