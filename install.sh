#!/bin/bash

current_directory=$PWD

printf "\n-----copying aion shell to /usr/bin...-----\n"

if [ ! -f /usr/bin/aion ]; then
	chmod +x /usr/bin/aion
	cp aion /usr/bin/
fi

printf "\n-----copying aion to /usr/local...-----\n"

cp -r aion-* /usr/local/

printf "\n-----copying aion_data to /etc...-----\n"

if [ ! -d "/etc/aion_data/" ]; then
	cp -r aion_data /etc/
fi

printf "\n-----creating directories if not existent\n"

if [ ! -d "/etc/aion_data/saves/" ]; then
  mkdir /etc/aion_data/saves/
fi

printf "\n-----moving install directory to /tmp...-----\n"

mkdir /tmp/aion_install
cd /tmp/aion_install

printf "\n-----updating the package list...-----\n"

apt-get -y update

printf "\n-----creating usb mountpoint...-----\n"

mkdir /mnt/usbstick

printf "\n-----installing and upgrading all required linux packages...-----\n"

apt-get -y install bison build-essential espeak ffmpeg flac git libasound2-dev libatlas-base-dev libpulse-dev python python-dev python-pip python3 python3-dev python3-pip python3-pyaudio sox subversion swig vlc wget
apt-get -y upgrade 

printf "\n-----patching vlc...-----\n"

sed -i 's/geteuid/getppid/' /usr/bin/vlc

rm -r /usr/lib/arm-linux-gnueabihf/vlc/lua/
svn checkout https://github.com/videolan/vlc/trunk/share/lua
mv lua/ /usr/lib/arm-linux-gnueabihf/vlc/

printf "\n-----setting audio volume...-----\n"

amixer cset numid=1 70%

printf "\n-----installing sphinxbase...-----\n"

wget https://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz/download -O sphinxbase.tar.gz

tar -xzvf sphinxbase.tar.gz

cd sphinxbase-5prealpha
./configure --enable-fixed
make
make install
cd ..

printf "\n-----installing pocketsphinx...-----\n"

wget https://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz/download -O pocketsphinx.tar.gz

tar -xzvf pocketsphinx.tar.gz

cd pocketsphinx-5prealpha
./configure
make
make install
cd ..

printf "\n-----installing snowboy...-----\n"

git clone https://github.com/Kitt-AI/snowboy

cd snowboy
python3 setup.py install

cd swig/Python3
make
cp -r snowboydetect.py _snowboydetect.so /usr/local/aion-*
cd ../..

cp -r resources /usr/local/aion-*

cd examples/Python3
cp snowboydecoder.py /usr/local/aion-*
cd ../../..

sed -i "s/from . import snowboydetect/import snowboydetect/g" /usr/local/aion-*/snowboydecoder.py

printf "\n-----installing pico2wave...-----\n"

wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico0_1.0+git20130326-9_armhf.deb
wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico-utils_1.0+git20130326-9_armhf.deb
apt-get -y install -f ./libttspico0_1.0+git20130326-9_armhf.deb ./libttspico-utils_1.0+git20130326-9_armhf.deb

printf "\n-----installing & upgrading all required python3 packages...-----\n"

yes | pip3 install --upgrade colorama pafy pocketsphinx psutil pyaudio pyudev SpeechRecognition Wikipedia-API youtube_dl

printf "\n-----changing permission-----\n"

chmod +x /usr/bin/aion

chmod +002 /etc/aion_data/config.xml
chmod -R 777 /etc/aion_data/config.xml

chmod +002 /etc/aion_data/language/
chmod -R 777 /etc/aion_data/language/

chmod +002 /etc/aion_data/logs/
chmod -R 777 /etc/aion_data/logs/

printf "\n-----removing the install directory from /tmp/...-----\n"

cd $current_directory

rm -r /tmp/aion_install

printf "\nInstallation completed. Please reboot the system to save all the changes\n"
