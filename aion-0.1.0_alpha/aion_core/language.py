#!/usr/bin/python3

try:
    from .config import Aion as _Aion
    from .utils import aion_data_path as _aion_data_path
except ImportError:
    from config import Aion as _Aion
    from utils import aion_data_path as _aion_data_path


def _language_file() -> str:
    """
    gets the language file for the current language

    :return: str
        return the language file for the current language
        syntax: "<language file>"
        example: "en_US"

    :since: 0.1.0
    """
    from colorama import Fore
    from os.path import isfile
    if isfile(language_directory + "/" + language + ".lng") is False:
        print(Fore.RED + "didn't found language file in your language. Using the default language file (en_US)" + Fore.RESET)
        return language_directory + "/en_US.lng"
    else:
        return language_directory + "/" + language + ".lng"


language = _Aion().get_language()
language_directory = _aion_data_path + "/language"
language_file = _language_file()
supported_languages = ["de_DE", "en_US"]


def add_entry(language_locale: str, skill: str, entry_dict: dict = {}) -> None:
    """
    adds an new entry(s) to from argument 'language_locale' given language

    :param language_locale: str
        language locale from the language to which the entry(s) is/are to be added
        syntax: <language locale>
        example: "de_DE"
    :param skill: str
        skill name to which the entry belongs
        syntax: "<skill name>"
        example: "test_skill"
    :param entry_dict: dict, optional
        all texts for execution of a function
        syntax: {<entry name>: <text of your entry>}
        example: {"test_entry": "Test function was executed correctly"}
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import language_lng_file_doesnt_exist, language_entry_already_exist
    except ImportError:
        from _error_codes import language_lng_file_doesnt_exist, language_entry_already_exist

    from os.path import isfile

    lng_file = language_directory + "/" + language_locale + ".lng"
    if isfile(lng_file) is False:
        raise FileNotFoundError("Errno: " + language_lng_file_doesnt_exist + " - The file " + lng_file + " doesn't exist")
    try:
        from .utils import BaseXMLWriter
    except ImportError:
        from utils import BaseXMLWriter

    lng_adder = BaseXMLWriter(lng_file)
    for entry, text in entry_dict.items():
        if exist_entry(language_locale, skill, entry) is True:
            raise IndexError("Errno: " + language_entry_already_exist + " - The entry " + entry + " already exist")
        lng_adder.add("<root>", skill + "." + str(entry), text=str(text))
    lng_adder.write()


def create_lng_file(language_locale: str, extra_dict: dict = {}, **extra: dict) -> None:
    """
    creates a new '.lng' file for given language locale with given entry_dict

    :param language_locale: str
        language locale of language from which the new file is to be created
        syntax: <language_locale>
        example: en_US
    :param extra_dict: dict, optional
        skill name you want to add specific entries
        syntax: {<name of the skill you want to add entries>: {{<name of the entry>: <text of the entry>}}
        example: {"test_skill": {"test_entry": "This is the text for the test text entry"}}
    :param extra: kwargs, optional
        skill name you want to add specific entries
        syntax: <name of the skill you want to add entries>={<name of the entry>: <text of the entry>}
        example: test_skill={"test_success": "The test was executed successfully", "text_error": "The test wasn't executed successfully"}
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import language_lng_file_already_exist
        from .utils import BaseXMLBuilder
    except ImportError:
        from _error_codes import language_lng_file_already_exist
        from utils import BaseXMLBuilder
    from os.path import isfile

    if isfile(language_directory + "/" + language_locale + ".lng"):
        raise FileExistsError("Errno: " + language_lng_file_already_exist + " - The language file " + language_locale + ".lng already exist in directory " + language_directory)

    lng_file = BaseXMLBuilder(language_locale)

    for skill, entry_dict in extra_dict.items():
        for entry_name, entry_text in entry_dict.items():
            lng_file.create_root_element(language_locale, str(skill) + "." + str(entry_name), text=str(entry_text))

    for skill, entry_dict in extra.items():
        for entry_name, entry_text in entry_dict.items():
            lng_file.create_root_element(language_locale, str(skill) + "." + str(entry_name), text=str(entry_text))
    lng_file.write(language_directory + "/" + language_locale + ".lng")


def delete_entry(language_locale: str, skill: str, entry_list: list = []) -> None:
    """
    deletes entries from '<language_locale>.lng'

    :param language_locale: str
        language locale from (file) which the entry is being deleted
        syntax: <language locale>
        example: "en_US"
    :param skill : str
        name of the skill from which the entries should be deleted
        syntax: <skill name>
        example: "test"
    :param entry_list: list, optional
        name of the entries you want to remove
        syntax: [<entry name>]
        example: ["test_entry"]
    :return: None

    :since: 0.1.0
    """
    try:
        from .utils import BaseXMLWriter
    except ImportError:
        from utils import BaseXMLWriter

    lng_writer = BaseXMLWriter(language_directory + "/" + language_locale + ".lng")
    for item in entry_list:
        lng_writer.remove("<root>", str(skill) + "." + str(item))
    lng_writer.write()


def exist_entry(language_locale: str, skill: str, entry: str) -> bool:
    """
    checks if a entry exist

    :param language_locale: str
        language locale from (file) which the entry should be search
        syntax: <language locale>
        example: "en_US"
    :param skill: str
        skill name from the entry
        syntax: <skill name>
        example: "test"
    :param entry: str
        entry name of skill (entry)
        syntax: <entry name>
        example: "test_entry"
    :return: bool
        returns True if entry exist / False if not
        syntax: <boolean>
        example: False

    :since: 0.1.0
    """
    try:
        from .utils import BaseXMLReader
    except ImportError:
        from utils import BaseXMLReader

    entry = entry.replace(" ", "_")

    lng_reader = BaseXMLReader(language_directory + "/" + language_locale + ".lng")
    for item in lng_reader.get_infos(["<root>"]).items().index(0):
        if skill + "." + entry in item["childs"]:
            return True
        else:
            return False


def start(skill: str, entry: str, format: dict = {}) -> str:
    """
    returns entry from given arguments

    :param skill: str
        name of the skill from the entry you want to call
        syntax: <skill name>
        example: "test_skill"
    :param entry: str
        name of the entry you want to call
        syntax: <entry>
        example: "test_func_entry"
    :param format: dict
        dictionary to format the string in the '.lng' file
        syntax: <format>
        example: {"test", "newtest"}: "This is a test" -> "This is a newtest"
    :return: str
        returns the (from 'format' formatted) string from the in '/etc/aion_data/config.xml' setted language locale '.lng' file
        syntax: <return string>
        example: "This is a test"

    :since: 0.1.0
    """
    from ast import literal_eval
    from random import choice

    try:
        from .utils import BaseXMLReader
    except ImportError:
        from utils import BaseXMLReader

    lng_reader = BaseXMLReader(language_file)
    for item in lng_reader.get_infos([skill + "." + entry]).values().index(0):
        try:
            if item["text"].startswith("[") and item["text"].endswith("]"):
                return str(choice(literal_eval(item["text"]))).format(**format)
            else:
                return str(item["text"]).format(**format)
        except SyntaxError:
            return str(item["text"]).format(**format)
