# FreeWifi gateway

It connects to a [FreeWifi](https://wifi.free.fr/) hotspot and shares the connection via a WPA2 protected Wifi network and the Ethernet port.

## Hardware
It uses:
- a Raspberry Pi B model. (Yes, the old one :)) with this printed case http://www.thingiverse.com/thing:608169
- a [TP-Link TL-WN722N](http://www.tp-link.com/en/products/details/cat-11_TL-WN722N.html) usb dongle
- a [55cm 2.4GHz Yagi antenna](https://www.aliexpress.com/item/Hot-RP-SMA-2-4GHz-25-DBi-Yagi-Wireless-WLAN-WiFi-Antenna-For-Modem-PCI-Card/32608303098.html) connected to the wifi dongle

## Software

### OS

I used [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) Lite from September 2016.

### Installation

```sh
wget https://github.com/ticapix/freewifi_gateway/archive/master.zip -O freewifi_gateway.zip
unzip freewifi_gateway.zip
cd freewifi_gateway-master
sudo ./setup.sh
```

### Configuration

A new local hostspot will be created. By default, the SSID is `Gateway` with password `freewifi`. It will bring you the configuration web page

## Details

```sh
        valid interface combinations:
                 * #{ managed, P2P-client } <= 2, #{ AP, mesh point, P2P-GO } <= 2,
                   total <= 2, #channels <= 1
```
