#!/bin/sh


echo "checking nodejs"
which node
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


npm install
