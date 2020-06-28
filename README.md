**_aion_ - a python programmed digital assistant**

- [Introduction](#introduction)
- [Installation](#installation)
- [Start](#start)
- [Tutorial](#tutorial)
- [Todo](#todo)
- [Other Projects](#other-projects)
- [License](#license)

# Introduction

**aion** is an python3 based digital assistant (voice assistant). It requires python 3.6 or higher and only runs on Linux / UNIX systems

# Installation

The installation need 1 - 2 GB free space

To install **aion** for Linux / UNIX (only tested on Raspberry Pi 3B+ with Raspberry Pi OS), type:

```
$ sudo apt-get upgrade && sudo apt-get update
$ sudo apt-get install git
$ sudo git clone https://github.com/blueshard-dev/aion
$ cd aion_project
$ sudo ./install.sh  # if this won't work, type 'sudo bash install.sh' instead
```

This will take a while (depending on your internet speed) and installs all required components

After the installation is completed, reboot your system

# Start

To start / run aion, type:
```
$ aion start
```
or
```
$ aion run
```

# Tutorial

- [Voice Commands](#voice-commands)
- [Command Line Commands](#command-line-commands)

### Voice Commands

To start aion say the activation word (`aion` default) and then a voice command, e.g. `aion, whats the current time?`.
To change your activation word, visit https://snowboy.kitt.ai/, create a `.pmdl` file with your new activation word
and place it into `/usr/local/<your aion version>/etc/` and change the text of the `hotword_file` key in `/etc/aion_data` to `/usr/local/<your aion version>/etc/<your new snowboy file>`

- en_US
  - cpu usage - gives the cpu usage back (after 10 test seconds)
  - ip address - gives the current ip address back (won't work properly when device is offline)
  - play <song name> - plays given song on youtube (may won't play the correct song)
  - ram usage - gives the ram usage back (after 10 test seconds)
  - tell & about <person, topic or something else> - gives wikipedia article about the searched person, topic or something else back
  - time - gives the current time back

- de_DE
  - erzähle & über <Person, Thema oder irgendetwas anderes> - gibt den Wikipedia Artikel über das Gesuchte zurück
  - ip-addresse - gibt die aktuelle IP Adresse zurück (wird nicht richtig funktionieren, wenn das Gerät kein Internet hat)
  - prozessor auslastung - gibt die Prozessorauslastung zurück (nach 10 Sekunden Testzeit)
  - spiele <lied name> - spielt gegebenes Lied auf Youtube ab (wird eventuell nicht das richtige Lied abspielen)
  - uhr - gibt die aktuelle Zeit zurück
  - zeit - gibt die aktuelle Zeit zurück

See `/etc/aion_data/language/<your language locale>.acph` for all voice commands (the xml tags are the voice commands)

### Command Line Commands

```
Usage:
    aion [command]

Commands:
    start                                   starts aion
    run                                     runs aion

    install <skill / plugin>                installs a skill or plugin
    uninstall <skill / plugin>              uninstalls a skill or plugin
    remove <skill / plugin>                 removes a skill or plugin
    update <skill / plugin>                 updates a skill or plugin
    version <skill / plugin>                version of a skill or plugin

    save <name>                             saves the current aion_data directory (with a name)
    load <version> [name]                   loads a saved aion_data directory (add optional name to save the current aion_data directory with this name)
    saves                                   shows all saved aion_data directory
    
    pid                                     shows the pid from the running aion process
    kill                                    kills aion
    stop                                    stops aion      

    pack <custom skill / plugin directory>  packs the given directory with a custom skill or plugin into one standalone file for installation
```

# Todo

- [ ] LED support for respeaker users
- [ ] other logger
- [ ] bluetooth module to connect with phone and play music
- [ ] better commandline support
- [ ] spotify support (for the "play" voice command)
- [ ] watcher process to monitor the main process
- [ ] tutorials
- [ ] better description for the classes and functions
- [ ] ai based speech recognition engine
- [ ] ai based text-to-speech engine

# Other Projects

- [x] support library (see [aionlib](https://github.com/blueShard-dev/aionlib))
- [ ] gui interface
- [ ] aion for windows
- [ ] (android) app for phones

# License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0) - see the [LICENSE](License) file for more details
