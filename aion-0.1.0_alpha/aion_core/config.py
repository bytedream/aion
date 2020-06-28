#!/usr/bin/python3

try:
    from .utils import aion_data_path as _aion_data_path, BaseXMLReader as _BaseXMLReader, BaseXMLWriter as _BaseXMLWriter
except ImportError:
    from utils import aion_data_path as _aion_data_path, BaseXMLReader as _BaseXMLReader, BaseXMLWriter as _BaseXMLWriter


config_file = _aion_data_path + "/config.xml"


class Aion:
    """
    get infos about all aion internal configs (and change them)

    :since: 0.1.0
    """

    def __init__(self) -> None:
        """
        set all class values

        :return: None

        :since: 0.1.0
        """
        self.all_listening_modes = ["auto", "manual"]
        self.all_stt_engines = ["google", "pocketsphinx"]
        self.all_time_formats = ["12", "24"]
        self.all_tts_engines = ["pico2wave", "espeak"]
        self.supported_languages = ["de_DE", "en_US"]

        self._aion_cfg_reader = _BaseXMLReader(config_file)
        self._aion_cfg_writer = _BaseXMLWriter(config_file)

    def get_hotword_file(self) -> str:
        """
        get set hotword file path

        :return: str
            returns path of the hotword file
            syntax: <hotword file path>
            example: "/usr/local/aion-<aion_version>/etc/Aion.pmdl"

        :since: 0.1.0
        """
        from glob import glob
        for value_list in self._aion_cfg_reader.get_infos(["hotword_file"]).values():
            for config in value_list:
                if config["parent"]["tag"] == "aion":
                    return glob(config["text"])[0]

    def get_language(self) -> str:
        """
        get set language locale

        :return: str
            returns language locale
            syntax: <language locale>
            example: "en_US"

        :since: 0.1.0
        """
        for value_list in self._aion_cfg_reader.get_infos(["language"]).values():
            for config in value_list:
                if config["parent"]["tag"] == "aion":
                    return config["text"]

    def get_listening_mode(self) -> str:
        """
        get set listening mode

        :return: str
            returns listening mode
            syntax: <listening mode>
            example: "auto"

        :since: 0.1.0
        """
        for value_list in self._aion_cfg_reader.get_infos(["listening_mode"]).values():
            for config in value_list:
                if config["parent"]["tag"] == "aion":
                    return config["text"]

    def get_pid_manipulation_number(self) -> int:
        """
        get set pid manipulation number

        :return: int
            returns the pid manipulation number
            syntax: <pid manipulation number>
            example: 4

        :since: 0.1.0
        """
        for value_list in self._aion_cfg_reader.get_infos(["pid_manipulation_number"]).values():
            for config in value_list:
                if config["parent"]["tag"] == "aion":
                    return int(config["text"])

    def get_stt_engine(self) -> str:
        """
        get set speech-to-text engine

        :return: str
            returns speech-to-text engine
            syntax: <speech-to-text engine>
            example: "google"

        :since: 0.1.0
        """
        for value_list in self._aion_cfg_reader.get_infos(["listening_source"]).values():
            for config in value_list:
                if config["parent"]["tag"] == "aion":
                    return config["text"]

    def get_time_format(self) -> int:
        """
        get set time format

        :return: str
            returns time format
            syntax: <time format>
            example: 24

        :since: 0.1.0
        """
        for value_list in self._aion_cfg_reader.get_infos(["time_format"]).values():
            for config in value_list:
                if config["parent"]["tag"] == "aion":
                    return int(config["text"])

    def get_tts_engine(self) -> str:
        """
        get set text-to-speech engine

        :return: str
            returns text-to-speech engine
            syntax: <text-to-speech engine>
            example: "espeak"

        :since: 0.1.0
        """
        for value_list in self._aion_cfg_reader.get_infos(["tts_engine"]).values():
            for config in value_list:
                if config["parent"]["tag"] == "aion":
                    return config["text"]

    @staticmethod
    def reset() -> None:
        """
        resets the aion config values

        :return: None

        :since: 0.1.0
        """
        from locale import getdefaultlocale

        _BaseXMLWriter(config_file).remove("config", "aion")
        aion_cfg_writer = _BaseXMLWriter(config_file)
        aion_cfg_writer.add("config", "aion")
        aion_cfg_writer.add("aion", "hotword_file", text="/usr/local/aion-*/etc/Aion.pmdl")
        aion_cfg_writer.add("aion", "language", text=str(getdefaultlocale()[0]))
        aion_cfg_writer.add("aion", "listening_mode", text="auto")
        aion_cfg_writer.add("aion", "pid_manipulation_number", text="4")
        aion_cfg_writer.add("aion", "stt_engine", text="pocketsphinx")
        aion_cfg_writer.add("aion", "time_format", text="12")
        aion_cfg_writer.add("aion", "tts_engine", text="espeak")
        aion_cfg_writer.write()

    def set_hotword_file(self, hotword_file: str) -> None:
        """
        sets the hotword file

        :param hotword_file: str
            location from the new hotword file
            syntax: <hotword_file>
           example: "/usr/local/aion-*/etc/Aion.pmdl"
        :return: None

        :since: 0.1.0
        """
        try:
            from ._error_codes import config_no_hotword_file_file
        except ImportError:
            from _error_codes import config_no_hotword_file_file
        from os.path import isfile

        if isfile(hotword_file):
            self._aion_cfg_writer.update("aion", "hotword_file", text=str(hotword_file))
            self._aion_cfg_writer.write()
        else:
            raise FileNotFoundError("Errno: " + config_no_hotword_file_file + " - Couldn't find file '" + hotword_file + "'")

    def set_language(self, language: str) -> None:
        """
        sets the language locale

        :param language: str
            new language locale
            syntax: <language locale>
            example: "en_US"
        :return: None

        :since: 0.1.0
        """
        from colorama import Fore

        if language in self.supported_languages:
            self._aion_cfg_writer.update("aion", "language", text=str(language))
            self._aion_cfg_writer.write()
        else:
            print(Fore.RED + "'" + language + "' isn't an official supported language for speech output (type 'aion.Config.supported_languages' to see all supported languages).\n"
                                              "The complete speech output is now in English. You have to create your own '.lng' file to support your language.\n" +
                                              str(self.supported_languages) + " are the supported languages" + Fore.RESET)
            self._aion_cfg_writer.update("aion", "language", text=str(language))
            self._aion_cfg_writer.write()

    def set_listening_mode(self, listening_mode: str) -> None:
        """
        sets the listening mode

        :param listening_mode: str
            new listening mode
            syntax: <listening mode>
            example: "auto"
        :return: None

        :since: 0.1.0
        """
        try:
            from ._error_codes import config_no_supported_listening_mode
        except ImportError:
            from _error_codes import config_no_supported_listening_mode

        if listening_mode in self.all_listening_modes:
            self._aion_cfg_writer.update("aion", "listening_mode", text=str(listening_mode))
            self._aion_cfg_writer.write()
        else:
            raise ValueError("Errno: " + config_no_supported_listening_mode + " - " + str(listening_mode) + " isn't a supported listening mode. Please choose from these: " + str(self.all_listening_modes))

    def set_pid_manipulation_number(self, pid_manipulation_number: int) -> None:
        """
        sets the pid manipulation number

        :param pid_manipulation_number: int
            new pid manipulation number
            syntax: <pid manipulation number>
            example: 4
        :return: None

        :since: 0.1.0
        """
        self._aion_cfg_writer.update("aion", "listening_mode", text=str(pid_manipulation_number))
        self._aion_cfg_writer.write()

    def set_stt_engine(self, stt_engine: str) -> None:
        """
        sets the speech-to-text engine

        :param stt_engine: str
            new speech-to-text engine
            syntax: <speech-to-text engine>
            example: "pocketsphinx"
        :return: None

        :since: 0.1.0
        """
        try:
            from ._error_codes import config_no_supported_listening_source
        except ImportError:
            from _error_codes import config_no_supported_listening_source

        if stt_engine in self.all_stt_engines:
            self._aion_cfg_writer.update("aion", "stt_engine", text=str(stt_engine))
            self._aion_cfg_writer.write()
        else:
            raise ValueError("Errno: " + config_no_supported_listening_source + " - " + str(stt_engine) + " isn't a supported listening source. Please choose from these: " + str(self.all_stt_engines))

    def set_time_format(self, time_format: str) -> None:
        """
        sets the time format

        :param time_format: str
            new time format
            syntax: <time format>
            example: "24"
        :return: None

        :since: 0.1.0
        """
        try:
            from ._error_codes import config_no_supported_time_format
        except ImportError:
            from _error_codes import config_no_supported_time_format

        if str(time_format) in self.all_time_formats:
            self._aion_cfg_writer.update("aion", "time_format", text=str(time_format))
            self._aion_cfg_writer.write()
        else:
            raise ValueError("Error: " + config_no_supported_time_format + " - " + str(time_format) + " isn't a supported time format. Please choose from these: " + str(self.all_time_formats))

    def set_tts_engine(self, tts_engine: str) -> None:
        """
        sets the text-to-speech engine

        :param tts_engine: str
            new text-to-speech engine
            syntax: <text-to-speech engine>
            example: "espeak"
        :return: None

        :since: 0.1.0
        """
        try:
            from ._error_codes import config_no_supported_tts_engine
        except ImportError:
            from _error_codes import config_no_supported_tts_engine

        if tts_engine in self.all_tts_engines:
            self._aion_cfg_writer.update("aion", "tts_engine", text=str(tts_engine))
            self._aion_cfg_writer.write()
        else:
            raise ValueError("Errno: " + config_no_supported_tts_engine + " - " +str(tts_engine) + " isn't a supported tts engine. Please choose from these: " + str(self.all_tts_engines))


def add_entry(name: str, text: str = None, attrib: dict = {}, parent_name: str = "config", parent_attrib: dict = {}) -> None:
    """
    adds an entry from the config file

    :param name: str
        name of the new entry
        syntax: <name>
        example: "test_entry"
    :param text: str, optional
        text of the new entry
        syntax: <text>
        example: "Test"
    :param attrib: dict, optional
        attributes of the new entry
        syntax: {<attribute name>: <attribute value>}
        example: {"test_attrib", "test"}
    :param parent_name: str, optional
        name of the parent entry to which the entry is added
        syntax: <parent name>
        example: "test_parent"
    :param parent_attrib: dict, optional
        attributes of the parent entry
        syntax: {<parent attribute name>: <parent attribute value>}
        example: {"version": "1.0.0"}
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import config_name_config_is_used_as_root_name, config_character_must_be_in_alphabet
    except ImportError:
        from _error_codes import config_name_config_is_used_as_root_name, config_character_must_be_in_alphabet

    cfg_writer = _BaseXMLWriter(config_file)

    if name == "config":
        raise NameError("Errno: " + config_name_config_is_used_as_root_name + " - Name 'config' is already used as root name")
    for char in name:
        if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_":
            raise IndexError("Errno: " + config_character_must_be_in_alphabet + " - " + char + " in " + name + " must be in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_'")

    cfg_writer.add(parent_name, name, text, attrib, parent_attrib=parent_attrib)
    cfg_writer.write()


def delete_entry(name: str, parent_name: str = "config", parent_attrib: dict = {}) -> None:
    """
    deletes an entry from the config file

    :param name: str
        name of the entry to be deleted
        syntax: <name>
        example: "test_entry"
    :param parent_name: str, optional
        name of the parent entry of the entry to be deleted
        syntax: <parent name>
        example: "test_parent"
    :param parent_attrib: dict, optional
        attributes of the parent entry from the entry to be searched
        syntax: {<attribute name>: <attribute value>}
        example: {"test_attrib", "test"}
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import config_root_tag_cannot_be_removed
    except ImportError:
        from _error_codes import config_root_tag_cannot_be_removed

    cfg_writer = _BaseXMLWriter(config_file)

    if name == "config":
        raise NameError("Errno: " + config_root_tag_cannot_be_removed + " - The root tag cannot be removed")

    cfg_writer.remove(parent_name, name, parent_attrib)
    cfg_writer.write()


def get_entry(name: str, parent_name: str = None, parent_attrib: dict = None) -> dict:
    """
    get infos about an entry

    :param name: str
        name of the entry to be searched
        syntax: <name>
        example: "test_entry"
    :param parent_name: str, optional
        name of the parent entry of the entry to be deleted
        syntax: <parent name>
        example: "test_parent"
    :param parent_attrib: dict, optional
        attributes of the parent entry
        syntax: {<attribute name>: <attribute value>}
        example: {"test_attrib", "test"}
    :return: dict
        returns the infos about the given entry
        syntax: {"text": <text of entry>, "attrib": <attributes of entry>}
        e.g.: {"text": "entry text", "attrib": {"version": "1.0.0"}}

    :since: 0.1.0
    """
    cfg_reader = _BaseXMLReader(config_file)
    return_dict = {}

    if parent_name:
        for value_list in cfg_reader.get_infos([name]).values():
            for entry in value_list:
                if entry["parent"] == parent_name:
                    if parent_attrib:
                        if entry["attrib"] == parent_attrib:
                            return_dict["text"] = entry["text"]
                            return_dict["attrib"] = entry["attrib"]
                            break
                    else:
                        return_dict["text"] = entry["text"]
                        return_dict["attrib"] = entry["attrib"]
                        break
    else:
        return_dict["text"] = cfg_reader.get_infos([name]).items().index(0)["text"]
        return_dict["attrib"] = cfg_reader.get_infos([name]).items().index(0)["attrib"]

    return return_dict


def update_entry(name: str, text: str = None, attrib: dict = {}, parent_name: str = "config", **extra: str) -> None:
    """
    updates an entry

    :param name: str
        name of the entry to be updated
        syntax: <name>
        example: "test_entry"
    :param text: str, optional
        new text of the entry to be updated
        syntax: <text>
        example: "new test text"
    :param attrib: dict, optional
        new attributes of the entry to be updated
        syntax: {<attribute name>: <attribute value>}
        example: {"new_test_attrib", "new_test"}
    :param parent_name: str, optional
        parent entry of the entry to be updated
        syntax: <parent name>
        example: "test_parent"
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import config_root_tag_cannot_be_updated
    except ImportError:
        from _error_codes import config_root_tag_cannot_be_updated

    cfg_writer = _BaseXMLWriter(config_file)

    if name == "config":
        raise NameError("Errno: " + config_root_tag_cannot_be_updated + " - Can't update root name")

    if extra:
        cfg_writer.update(parent_name, name, text, {**attrib, **extra})
    else:
        cfg_writer.update(parent_name, name, text, attrib)
