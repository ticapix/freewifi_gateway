#!/bin/sh

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
cp ./freewifi_gateway.daemon /etc/init.d/freewifi_gateway
chmod +x /etc/init.d/freewifi_gateway
NAME="freewifi_gateway"
PIDFILE="/var/run/$NAME.pid"
DAEMON="`pwd`/venv3/bin/python"
DAEMON_ARGS="`pwd`/run.py --pidfile $PIDFILE"
cat >> /etc/init.d/freewifi_gateway <<EOF
NAME="$NAME"
PIDFILE="$PIDFILE"
DAEMON="$DAEMON"
DAEMON_ARGS="$DAEMON_ARGS"
EOF
