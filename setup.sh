#!/bin/sh

dpkg -l firmware-atheros | grep --quiet '20160824-1'
if [ $? -ne 0 ]; then
    echo "installing new atheros firmware 20160824-1"
    cd /tmp/
    wget http://ftp.fr.debian.org/debian/pool/non-free/f/firmware-nonfree/firmware-atheros_20160824-1_all.deb
    dpkg -i firmware-atheros_20160824-1_all.deb
    cd -
fi

echo "checking nodejs"
which node > /dev/null
if [ $? -ne 0 ]; then
    echo "nodejs not installed"
    uname -m | grep --quiet armv6l
    if [ $? -ne 0 ]; then
	echo "trying default installer"
	curl -sL https://deb.nodesource.com/setup_6.x | bash -
	apt install -y nodejs
    else
	echo "armv6 detected. ugly install in /usr/local/"
	curl -sL https://nodejs.org/dist/v6.7.0/node-v6.7.0-linux-armv6l.tar.xz | tar --directory /usr/local/ --strip-components=1 -xvJf -
    fi
fi

echo "installing dependencies"
#npm install phantomjs

echo "checking for the python virtual environment"
if [ ! -d venv3 ]; then
    echo "creating one"
    python3 -m venv venv3
fi

. venv3/bin/activate

echo "installing dependencies"
pip install -r requirements.txt

echo "installing daemon"
