#!/bin/bash

if [ "$#" -gt "1" ]; then
    echo "too many arguments were given"
elif [ "$#" -eq "1" ]; then
    if [ "$1" == "--all" ]; then
		yes | pip3 uninstall aionlib colorama pafy pocketsphinx psutil pyaudio pyudev snowboy SpeechRecognition Wikipedia-API youtube_dl

        apt-get -y purge bison build-essential espeak ffmpeg flac libasound2-dev libatlas-base-dev libpulse-dev python3-pyaudio sox subversion swig vlc wget
        apt-get -y autoremove
		
		rm -r /usr/local/aion-*
		
        rm -r /etc/aion_data

        rm /usr/bin/aion
	  else
	      echo "unexpected argument were given"
		    exit 1
	  fi
else
    yes | pip3 uninstall aionlib colorama pafy pocketsphinx psutil pyaudio pyudev snowboy SpeechRecognition Wikipedia-API youtube_dl

    apt-get -y remove bison build-essential espeak ffmpeg flac libasound2-dev libatlas-base-dev libpulse-dev python3-pyaudio sox subversion swig vlc wget
	
	  rm -r /usr/local/aion-*
fi
