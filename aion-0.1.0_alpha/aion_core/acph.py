#!/usr/bin/python3

try:
    from .config import Aion as _Aion
    from .utils import aion_data_path as _aion_data_path
except ImportError:
    from config import Aion as _Aion
    from utils import aion_data_path as _aion_data_path


def _acph_file() -> str:
    """
    gets the activate phrase file for the current language

    :return: None

    :since: 0.1.0
    """
    from colorama import Fore
    from os.path import isfile
    if isfile(acph_directory + "/" + language + ".acph") is False:
        print(Fore.RED + "didn't found acph file in your language. Using the default acph file (en_US)" + Fore.RESET)
        return acph_directory + "/en_US.acph"
    else:
        return acph_directory + "/" + language + ".acph"


language = _Aion().get_language()
acph_directory = _aion_data_path + "/language"
acph_file = _acph_file()
supported_languages = ["de_DE", "en_US"]


def add_acph(language_locale: str, skill: str, acph_dict: dict = {}) -> None:
    """
    adds an new entry(s) to from argument 'language_locale' given language

    :param language_locale: str
        language locale from the language to which the entry(s) is/are to be added
        syntax: <language locale>
        example: "de_DE"
    :param skill: str
        skill name to which the acph belongs
        syntax: "<skill name>"
        example: "test_skill"
    :param acph_dict: dict, optional
        defines a word or a sentence from which a method is called
        syntax: {<activate phrase>: <method that should get called after the activate phrase was said>}
        example: {"start test": "MyTestMethod"}
        NOTE: in key 'activate_phrase' you can use the '__and__' statement. This checks if the words before and after '__and__' are in the sentence that the user has spoken in
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import acph_activate_phrase_exist
        from .utils import BaseXMLWriter
    except ImportError:
        from _error_codes import acph_activate_phrase_exist
        from utils import BaseXMLWriter

    acph_writer = BaseXMLWriter(acph_directory + "/" + language_locale + ".acph")
    for acph, method in acph_dict:
        if exist_acph(language_locale, acph):
            raise IndexError("Errno: " + acph_activate_phrase_exist + " - The activate phrase " + acph + " already exist")
        acph_writer.add("<root>", acph, skill=skill, method=method)
    acph_writer.write()


def create_acph_file(language_locale: str, skill_acph_dict_dict: dict = {}) -> None:
    """
    creates a new '.acph' file for given language locale with given skill_acph_dict_dict

    :param language_locale: str
        language locale of language from which the new file is to be created
        syntax: <language_locale>
        example: "en_US"
    :param skill_acph_dict_dict: dict, optional
        skill name you want to add specific entries
        syntax: {<skill name>: {<activate phrase>: <method that should get called after the activate phrase was said>}}
        example: {"test_skill": {"start test": "MyTestMethod"}}
        NOTE: in key 'activate_phrase' you can use the '__and__' statement. This checks if the words before and after '__and__' are in the sentence that the user has spoken in
    :return: None

    :since: 0.1.0
    """
    try:
        from .utils import BaseXMLBuilder
    except ImportError:
        from utils import BaseXMLBuilder

    acph_builder = BaseXMLBuilder(language_locale)
    for skill, acph_dict in skill_acph_dict_dict.items():
        for acph, method in acph_dict.items():
            acph_builder.create_root_element(acph, skill=skill, method=method)

    acph_builder.write(acph_directory + "/" + language_locale + ".acph")


def delete_acph(language_locale: str, acph_list: list = []) -> None:
    """
    deletes entries from '<language_locale>.acph'

    :param language_locale: str
        language locale from (file) which the activate phases is being deleted
        syntax: <language locale>
        example: "en_US"
    :param acph_list: list, optional
        name of the activate phases you want to remove
        syntax: [<activate phase name>]
        example: ["test_acph"]
    :return: None

    :since: 0.1.0
    """
    try:
        from .utils import BaseXMLWriter
    except ImportError:
        from utils import BaseXMLWriter

    acph_writer = BaseXMLWriter(acph_directory + "/" + language_locale + ".acph")
    for item in acph_list:
        acph_writer.remove("<root>", str(item))
    acph_writer.write()


def exist_acph(language_locale: str, acph: str) -> bool:
    """
    checks if a entry exist

    :param language_locale: str
        language locale from (file) which the activate phrase should be search
        syntax: <language locale>
        example: "en_US"
    :param acph: str
        activate phrase you want to check if exists
        syntax: <acph name>
        example: "start test"
    :return: bool
        returns True if acph exist / False if not
        syntax: <boolean>
        example: False

    :since: 0.1.0
    """
    try:
        from .utils import BaseXMLReader
    except ImportError:
        from utils import BaseXMLReader

    acph = acph.replace(" ", "_")

    acph_reader = BaseXMLReader(acph_directory + "/" + language_locale + ".acph")
    for item in acph_reader.get_infos(["<root>"]).items().index(0):
        if acph in item["childs"]:
            return True
        else:
            return False
