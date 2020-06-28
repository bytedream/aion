#!/usr/bin/python3

__author__ = "blueShard"
__license__ = "GPL-3.0"
__version__ = "0.1.0"

try:
    from .utils import aion_data_path, aion_path
except ImportError:
    from utils import aion_data_path, aion_path


def speech_output(speech_output: str) -> None:
    """
    plays a output of an artificial voice from the given words

    :param speech_output: str
        the words to be said
        syntax: <speech output words>
        example: "This is an test"
    :return: None

    :since: 0.1.0
    """
    try:
        from .config import Aion
    except ImportError:
        from config import Aion
    from os import system

    try:
        tts_engine = Aion().get_tts_engine()
    except IndexError:
        Aion().reset()
        tts_engine = Aion().get_tts_engine()

    if tts_engine == "espeak":
        system("espeak -v" + Aion().get_language().split("_")[0] + " " + str(speech_output) + " stdout | aplay")
        print("Sayed '" + str(speech_output) + "'")
    elif tts_engine == "pico2wave":
        system('pico2wave --lang=' + Aion().get_language().split("_")[0] + '-' + Aion().get_language().split("_")[1] + ' --wave=/tmp/aion.wav "' + str(speech_output) + "." + '"; aplay /tmp/aion.wav; rm /tmp/aion.wav')
        print("Sayed '" + str(speech_output) + "'")


def start(sudo: bool = False) -> None:
    """
    starts aion

    :param sudo: bool
        says if 'aion' should run as sudo (True) or not (False)
        syntax: <sudo>
        example: False
    :return: None

    :since: 0.1.0
    """
    from os import system
    if sudo is True:
        system("sudo python3 " + aion_path + "/main.py")
    else:
        system("python3 " + aion_path + "/main.py")


class ExecuteAionFile:

    """
    base class for execution '.aion' files

    :since: 0.1.0
    """

    def __init__(self, fname: str) -> None:
        """
        makes the file available for all functions in this class and calls the '_main()' function

        :param fname: str
            path of the file
            syntax: <filename>
            example: "/home/pi/test.aion"
        :return: None

        :since: 0.1.0
        """
        self.fname = fname

        self._main()

    def _main(self) -> None:
        """
        checks which type of an 'aion' file is the given file

        :return: None

        :since: 0.1.0
        """
        try:
            from ._error_codes import init_no_file_type
            from .utils import remove_space
        except ImportError:
            from _error_codes import init_no_file_type
            from utils import remove_space

        for line in open(self.fname, "r"):
            if line.isspace():
                continue
            elif line.startswith("#"):
                line = remove_space(line, "")
                if line.startswith("#type:"):
                    line = line.replace("#type:", "")
                    if line.strip() == "skill":
                        self._skill()
                    elif "plugin" in line.strip():
                        self._plugin()
            else:
                raise IndexError("Errno: " + init_no_file_type + " - Couldn't find file type in " + self.fname)

    def _plugin(self) -> None:
        """
        execute the given file as plugin type

        :return: None

        :since: 0.1.0
        """
        try:
            from .plugin import execute_aion_file_type_plugin
        except ImportError:
            from plugin import execute_aion_file_type_plugin
        execute_aion_file_type_plugin(self.fname)

    def _skill(self) -> None:
        """
        execute the given file as skill type

        :return: None

        :since: 0.1.0
        """
        try:
            from .skill import execute_aion_file_type_skill
        except ImportError:
            from skill import execute_aion_file_type_skill
        execute_aion_file_type_skill(self.fname)
