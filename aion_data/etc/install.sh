#!/bin/bash

if [ ! -d "/usr/local/aion-"]; then
	apt-get install git
	git --clone https://github.com/blueShard-dev/aion /tmp/aion_installation
	bash /tmp/aion_installation/install.sh
	
	rm -r /tmp/aion_installation
else
	echo "Aion is already installed"
fi
