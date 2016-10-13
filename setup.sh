#!/bin/sh

cd `pwd`/$(dirname $0)

#apt-get install -y iw iproute2 hostapd dnsmasq python3-venv systemd

dpkg -l firmware-atheros | grep --quiet '20160824-1'
if [ $? -ne 0 ]; then
    echo "installing new atheros firmware 20160824-1"
    cd /tmp/
    wget http://ftp.fr.debian.org/debian/pool/non-free/f/firmware-nonfree/firmware-atheros_20160824-1_all.deb
    dpkg -i firmware-atheros_20160824-1_all.deb
    cd -
fi

echo "checking for the python virtual environment"
if [ ! -d venv3 ]; then
    echo "creating one"
    python3 -m venv venv3
fi

. venv3/bin/activate

echo "installing dependencies"
#pip install -r requirements.txt

echo "installing daemon"
cat > `pwd`/freewifi_gateway.service <<EOF
[Unit]
Description=FreeWifi Gateway service
After=network.target
Before=network.target

[Service]
Type=simple
WorkingDirectory=`pwd`
ExecStart=`pwd`/venv3/bin/python -m freewifi_gateway
Restart=on-failure
RestartSec=42

[Install]
WantedBy=multi-user.target
EOF

systemctl enable "`pwd`/freewifi_gateway.service"
systemctl restart freewifi_gateway.service
