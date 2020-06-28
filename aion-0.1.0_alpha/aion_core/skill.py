#!/usr/bin/python3

try:
    from .utils import aion_data_path as _aion_data_path
except ImportError:
    from utils import aion_data_path as _aion_data_path


skills_path = _aion_data_path + "/skills"
skills_file = skills_path + "/skills.xml"


class Skill:
    """
    base class for use custom skills

    :since: 0.1.0
    """

    def __init__(self, activate_phrase: str, speech_input: str, run_after_plugins: dict, run_before_plugins: dict) -> None:
        """
        :param activate_phrase: str
            activate phrase that called this class
            syntax: "<activate phrase>"
            example: "test"
        :param speech_input: str
            complete spoken words
            syntax: "<speech input>"
            example: "Start the test"
        :param run_after_plugins: dict
            all run after plugins
        :param run_before_plugins: dict
            all run before plugins
        :return: None

        :since: 0.1.0
        """
        self.activate_phrase = activate_phrase
        self.speech_input = speech_input

        try:
            self.run_after_plugins = run_after_plugins[self.__class__.__name__]
        except KeyError:
            self.run_after_plugins = {}
        try:
            self.run_before_plugins = run_before_plugins[self.__class__.__name__]
        except KeyError:
            self.run_before_plugins = {}

    def main(self) -> None:
        """
        gets called if user says the defined activate_phrase

        :return: None

        :since: 0.1.0
        """
        pass

    def run_after(self) -> None:
        """
        gets called after the 'main' function was executed

        :return: None

        :since: 0.1.0
        """
        pass

    def run_before(self) -> None:
        """
        gets called before the 'main' function was executed

        :return: None

        :since: 0.1.0
        """
        pass

    def start_run_after_plugin(self, plugin_name: str) -> None:
        """
        calls a 'run_after' plugin (all plugins are in at the root of 'run_after_plugins' dict)

        :param plugin_name: str
            name of the plugin that should called (all plugins are in at the root of 'run_after_plugins' dict)
            syntax: "<plugin name>"
            example: "ExampleClass
        :return: None

        :since: 0.1.0
        """
        try:
            from .plugin import _run_befater_plugin, RUN_AFTER
        except ImportError:
            from plugin import _run_befater_plugin, RUN_AFTER

        if plugin_name in self.run_after_plugins:
            _run_befater_plugin(RUN_AFTER, plugin_name, self.run_after_plugins[plugin_name]["method"], self.activate_phrase, self.speech_input)

    def start_run_before_plugin(self, plugin_name: str) -> None:
        """
        calls a 'run_before' plugin (all plugins are in at the root of 'run_before_plugins' dict)

        :param plugin_name: str
            name of the plugin that should called (all plugins are in at the root of 'run_before_plugins' dict)
            syntax: "<plugin name>"
            example: "ExampleClass"
        :return: None

        :since: 0.1.0
        """
        try:
            from .plugin import _run_befater_plugin, RUN_BEFORE
        except ImportError:
            from plugin import _run_befater_plugin, RUN_BEFORE

        if plugin_name in self.run_before_plugins:
            _run_befater_plugin(RUN_BEFORE, plugin_name, self.run_before_plugins[plugin_name]["method"], self.activate_phrase, self.speech_input)

    def speech_output(self, speech_output: str) -> None:
        """
        plays a output of an artificial voice from the given words

        :param speech_output: str
            the words to be said
            syntax: "<speech output words>"
            example: "This is an test"
        :return: None

        :since: 0.1.0
        """
        try:
            from . import speech_output as _speech_output
        except ImportError:
            from .__init__ import speech_output as _speech_output

        _speech_output(speech_output)


def create_skill_file(activate_phrases: dict,
                      author: str,
                      language_locales: list,
                      skill_name: str,
                      main_file: str,
                      version: str,
                      additional_directories: list = [],
                      description: str = "",
                      language_dict: dict = {},
                      license: str = "",
                      required_python3_packages: list = []) -> None:
    """
    creates a file from which a skill can be installed

    :param activate_phrases: dict
        defines a word or a sentence from which a method is called
        syntax: {<activate phrase>: <method that should get called after the activate phrase was said>}
        example: {"start test": "MyTestMethod"}
        NOTE: in key 'activate_phrase' you can use the '__and__' statement. This checks if the words before and after '__and__' are in the sentence that the user has spoken in
    :param author: str
        name of the author from the skill
        syntax: <author name>
        example: "blueShard"
    :param language_locales: list
        list of language locales for which the skill is available
        syntax: [<language locale>]
        example: ["en_US"]
    :param main_file: str
        file name of file where all methods for the activate_phrases are defined
        syntax: <file name>
        example: "test.py"
        NOTE: the file must be in the same directory as the file from which 'create_skill_file' is being executed
    :param skill_name: str
        name of the skill you create
        syntax: <skill name>
        example: "text_skill"
    :param version: str
        version (number) of your skill
        syntax: <version>
        example: "1.0.0"
    :param additional_directories: list, optional
        list of additional directories your main file needs for execution
        syntax: [<additional directories>]
        example: ["test_directory"]
        NOTE: the directories must be in the same directory as the file from which 'create_skill_file' is being executed
    :param description: str, optional
        description of your skill
        syntax: <description>
        example: "A simple skill to test the method 'create_skill_file'"
    :param language_dict: dict, optional
        dictionary of messages which are saved in (from argument 'language_locales' given) '.lng' files
        syntax: {<entry>, <text>}
        example: {"test_entry": "The test was successful"}
        NOTE: the method name should be included in the entry for legibility
        NOTE2: for more infos about language ('.lng') files, see file 'language.py'
    :param license: str, optional
        license of the skill
        syntax: <license>
        example: "MPL-2.0"
    :param required_python3_packages: list, optional
        list of python3 packages your package needs for correct execution
        syntax: [<python3 package>]
        example: ["aionlib"]
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import skill_author_must_be_str, skill_language_locales_must_be_list_or_tuple, skill_skill_name_must_be_str, skill_main_file_must_be_str, skill_main_file_not_found,\
            skill_main_file_name_must_be_skill_name, skill_version_must_be_str, skill_additional_directories_must_be_list_or_tuple, skill_couldnt_find_additional_directories_directory,\
            skill_description_must_be_str, skill_language_dict_must_be_dict, skill_language_dict_character_must_be_in_alphabet, skill_license_must_be_str,\
            skill_required_python3_package_must_be_list_or_tuple, skill_activate_phrases_must_be_dict, skill_activate_phrases_character_must_be_in_alphabet
    except ImportError:
        from _error_codes import skill_author_must_be_str, skill_language_locales_must_be_list_or_tuple, skill_skill_name_must_be_str, skill_main_file_must_be_str, skill_main_file_not_found,\
            skill_main_file_name_must_be_skill_name, skill_version_must_be_str, skill_additional_directories_must_be_list_or_tuple, skill_couldnt_find_additional_directories_directory,\
            skill_description_must_be_str, skill_language_dict_must_be_dict, skill_language_dict_character_must_be_in_alphabet, skill_license_must_be_str,\
            skill_required_python3_package_must_be_list_or_tuple, skill_activate_phrases_must_be_dict, skill_activate_phrases_character_must_be_in_alphabet

    from os import getcwd, listdir

    write_dict = {}

    if isinstance(author, str) is False:
        raise TypeError("Errno: " + skill_author_must_be_str + " - Argument 'author' must be str, got " + type(author).__name__)
    write_dict["author"] = author

    if isinstance(language_locales, (list, tuple)) is False:
        raise TypeError("Errno: " + skill_language_locales_must_be_list_or_tuple + " - Argument 'language_locales' must be list or tuple, got " + type(language_locales).__name__)
    write_dict["language_locales"] = language_locales

    if isinstance(skill_name, str) is False:
        raise TypeError("Errno: " + skill_skill_name_must_be_str + " - Argument 'skill_name' must be str, got " + type(skill_name).__name__)
    write_dict["skill_name"] = skill_name

    if isinstance(main_file, str) is False:
        raise TypeError("Errno: " + skill_main_file_must_be_str + " - Argument 'main_file' must be str, got " + type(author).__name__)
    if main_file not in listdir(getcwd()):
        raise FileNotFoundError("Errno: " + skill_main_file_not_found + " - Couldn't find the file " + main_file + " in current directory")
    if main_file[:-3] == skill_name is False:
        raise NameError("Errno: " + skill_main_file_name_must_be_skill_name + " - The file name from " + main_file + " must be same as the argument 'name' (" + skill_name + ")")
    write_dict["main_file"] = main_file

    if isinstance(version, str) is False:
        raise TypeError("Errno: " + skill_version_must_be_str + " - Argument 'version' must be str, got " + type(version).__name__)
    write_dict["version"] = version

    # ----- #

    if isinstance(additional_directories, (list, tuple)) is False:
        raise TypeError("Errno: " + skill_additional_directories_must_be_list_or_tuple + " - Argument 'additional_directories' must be list or tuple, got " + type(additional_directories).__name__)
    for directory in additional_directories:
        if directory not in listdir(getcwd()):
            raise NotADirectoryError("Errno: " + skill_couldnt_find_additional_directories_directory + " - Couldn't find the directory " + directory + " in current directory")
    write_dict["additional_directories"] = additional_directories

    if isinstance(description, str) is False:
        raise TypeError("Errno: " + skill_description_must_be_str + " - Argument 'description' must be str, got " + type(description).__name__)
    write_dict["description"] = description

    if isinstance(language_dict, dict) is False:
        raise TypeError("Errno: " + skill_language_dict_must_be_dict + " - Argument 'language_success' must be dict, got " + type(language_dict).__name__)
    for key in language_dict.keys():
        tmp_string = ""
        for char in key:
            if char == " ":
                char = "_"
            if char.lower() not in "abcdefghijklmnopqrstuvwxyz_":
                raise ValueError("Errno: " + skill_language_dict_character_must_be_in_alphabet + " - Setter " + str(char) + " in " + str(key) + " must be in 'ABCDEFGHIJLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyz_'")
            tmp_string = tmp_string + char
        language_dict[tmp_string] = language_dict.pop(key)
    write_dict["language_dict"] = language_dict

    if isinstance(license, str) is False:
        raise TypeError("Errno: " + skill_license_must_be_str + " - Argument 'license' must be str, got " + type(license).__name__)
    write_dict["license"] = license

    if isinstance(required_python3_packages, (list, tuple)) is False:
        raise TypeError("Errno: " + skill_required_python3_package_must_be_list_or_tuple + " - Argument 'required_python3_packages' must be list or tuple, got " + type(required_python3_packages).__name__)
    write_dict["required_python3_packages"] = required_python3_packages

    # ----- #

    if isinstance(activate_phrases, dict) is False:
        raise TypeError("Errno: " + skill_activate_phrases_must_be_dict + " - Argument 'activate_phrases' must be dict, got " + type(activate_phrases).__name__)
    for item in activate_phrases:
        tmp_string = ""
        for char in item:
            if char == " ":
                char = "_"
            if char.lower() not in "abcdefghijklmnopqrstuvwxyz-_":
                raise ValueError("Errno: " + skill_activate_phrases_character_must_be_in_alphabet + " - Letter " + str(char) + " in " + str(item) + " must be in 'ABCDEFGHIJLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyz-_'")
            tmp_string = tmp_string + char
        activate_phrases[tmp_string] = activate_phrases.pop(item)
    write_dict["activate_phrases"] = activate_phrases

    # ----- #

    with open("skill.aion", "w") as file:
        file.write("#type: skill\n")
        for key, value in write_dict.items():
            file.write(key + " = " + str(value) + "\n")
        file.close()


def create_skill_package(dir_name: str) -> None:
    """
    creates a stand alone file ('.skill') from given directory

    :param dir_name: str
        directory name of the directory from which you want to create a '.skill' file
        syntax: <directory name>
        example: "/home/pi/test/"
    :return: None

    :note: 'skill.aion' file must be in the given directory (see 'create_skill_file' to create a 'skill.aion' file)

    :since: 0.1.0
    """
    try:
        from ._error_codes import skill_package_couldnt_find_directory, skill_package_couldnt_find_aion_file, skill_package_expected_one_aion_file
    except ImportError:
        from _error_codes import skill_package_couldnt_find_directory, skill_package_couldnt_find_aion_file, skill_package_expected_one_aion_file

    from os import listdir, mkdir, rename
    from os.path import isdir
    from random import sample
    from shutil import make_archive, rmtree

    if isdir(dir_name) is False:
        raise NotADirectoryError("Errno: " + skill_package_couldnt_find_directory + " - Couldn't find the directory '" + dir_name + "'")

    name = ""
    file_num = 0
    for file in listdir(dir_name):
        if file.endswith(".aion"):
            file_num += 1
            name = "".join(file.split(".aion")[0])
    if file_num == 0:
        raise FileNotFoundError("Errno: " + skill_package_couldnt_find_aion_file + " - Couldn't find .aion file in " + dir_name + ". To create one use the 'create_skill_file' function in aionlib.skill")
    elif file_num > 1:
        raise FileExistsError("Errno: " + skill_package_expected_one_aion_file + " - Expected one .aion file in " + dir_name + ", got " + str(file_num))

    skill_dir_name = "skill_" + name + "".join([str(num) for num in sample(range(1, 10), 5)])
    mkdir(skill_dir_name)

    make_archive(name + ".skill", "zip", skill_dir_name)
    rename(skill_dir_name + ".skill.zip", skill_dir_name + ".skill")

    rmtree(skill_dir_name)


def execute_aion_file_type_skill(fname: str) -> None:
    """
    installs custom skill from '<file name>.aion'

    :param fname: str
        file name of the '.aion' file
        syntax: <file name>
        example: "/home/pi/skill.aion"
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import skill_couldnt_find_key, skill_skill_already_exist, skill_file_doesnt_exist, skill_directory_doesnt_exist, skill_directory_already_exist, \
            skill_couldnt_install_python3_package
        from .acph import add_acph
        from .language import add_entry, language_directory
        from .utils import BaseXMLReader, BaseXMLWriter
    except ImportError:
        from acph import add_acph
        from language import add_entry, language_directory
        from utils import BaseXMLReader, BaseXMLWriter
        from _error_codes import skill_couldnt_find_key, skill_skill_already_exist, skill_file_doesnt_exist, skill_directory_doesnt_exist, skill_directory_already_exist, \
            skill_couldnt_install_python3_package

    from ast import literal_eval
    from importlib import import_module
    from os import listdir, path
    from shutil import copy, copytree
    from subprocess import call
    setup_dict = {}
    setup_dir = path.dirname(path.abspath(fname))
    for line in open(fname, "r"):
        if line.startswith("#"):
            continue
        setup_dict[line.split("=")[0].strip()] = line.split("=")[1].strip()
    try:
        activate_phrases = literal_eval(setup_dict["activate_phrases"])
        author = setup_dict["author"]
        language_locales = literal_eval(setup_dict["language_locales"])
        main_file = setup_dict["main_file"]
        skill_name = setup_dict["skill_name"]
        version = setup_dict["version"]

        additional_directories = literal_eval(setup_dict["additional_directories"])
        description = setup_dict["description"]
        language_dict = literal_eval(setup_dict["language_dict"])
        license = setup_dict["license"]
        required_python3_packages = literal_eval(setup_dict["required_python3_packages"])
    except KeyError as error:
        raise KeyError("Errno: " + skill_couldnt_find_key + " - Couldn't find key " + str(error) + " in " + fname)

    # ----- #

    if skill_name in get_all_skills():
        raise NameError("Errno: " + skill_skill_already_exist + " - The skill " + skill_name + " already exist")

    if path.isfile(setup_dir + "/" + main_file) is False:
        raise FileNotFoundError("Errno: " + skill_file_doesnt_exist + " - The file " + main_file + " doesn't exist in setup dir (" + setup_dir + ")")

    for directory in additional_directories:
        if path.isdir(setup_dir + "/" + directory) is False:
            raise NotADirectoryError("Errno: " + skill_directory_doesnt_exist + " - The directory " + directory + " doesn't exist in setup dir (" + setup_dir + ")")
        if directory in listdir(skills_path):
            raise IsADirectoryError("Errno: " + skill_directory_already_exist + " - The directory " + directory + " already exist in " + skills_path)

    # ----- #

    for package in required_python3_packages:
        call("pip3 install " + package, shell=True)
        try:
            import_module(package)
        except ModuleNotFoundError:
            raise ModuleNotFoundError("Errno: " + skill_couldnt_install_python3_package + " - Couldn't install the required python3 package '" + package + "'")

    copy(main_file, skills_path + "/" + main_file)

    for directory in additional_directories:
        copytree(directory, skills_path + "/" + directory)

    for language in language_locales:
        add_acph(language, skill_name, activate_phrases)
        add_entry(language, skill_name, language_dict)

    dat_writer = BaseXMLWriter(skills_file)

    dat_writer.add("<root>", str(skill_name), author=str(author))
    dat_writer.add(str(skill_name), "activate_phrases", str(activate_phrases))
    dat_writer.add(str(skill_name), "additional_directories", str(additional_directories))
    dat_writer.add(str(skill_name), "description", str(description))
    dat_writer.add(str(skill_name), "language_dict", str(language_dict))
    dat_writer.add(str(skill_name), "language_locales", str(language_locales))
    dat_writer.add(str(skill_name), "license", str(license))
    dat_writer.add(str(skill_name), "main_file", str(main_file))
    dat_writer.add(str(skill_name), "required_python3_packages", str(required_python3_packages))
    dat_writer.add(str(skill_name), "version", str(version))
    dat_writer.write()


def execute_skill_file(fname: str) -> None:
    """
    executes a '<name>.skill' file for installing custom skills

    :param fname: str
        file name of the '.skill' file
        syntax: <fname>
        example: "/home/pi/test.skill"
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import skill_couldnt_find_skill_dot_aion
    except ImportError:
        from _error_codes import skill_couldnt_find_skill_dot_aion

    from glob import glob
    from os.path import isfile
    from zipfile import ZipFile
    with ZipFile(fname, "r") as zipfile:
        zipfile.extractall("/tmp")
        zipfile.close()
    if isfile(glob("/tmp/skill_*/skill.aion")[0]) is False:
        raise FileNotFoundError("Errno: " + skill_couldnt_find_skill_dot_aion + " - ouldn't find 'skill.aion' in " + fname)
    else:
        execute_aion_file_type_skill(glob("/tmp/skill_*/skill.aion")[0])


def get_all_skills() -> list:
    """
    returns all installed skills

    :return: list
        returns list of all installed skills
        syntax: [<skill>]
        example: ["skills"]

    :since: 0.1.0
    """
    try:
        from .utils import BaseXMLReader
    except ImportError:
        from utils import BaseXMLReader
    return BaseXMLReader(skills_file).get_infos("<root>").items().index(0)[0]["childs"]


def get_skill_infos(skill_name: str) -> dict:
    """
    returns infos about an given skill

    :param skill_name: str
        name of the skill you want to get infos about
        syntax: <skill name>
        example: "test_skill"
    :return: dict
        returns a dictionary with infos of the skill
        syntax: {"activate_phrases": {<activate phrases>},
                "author": <author>,
                "language_locales": [<language locales>],
                "main_file": <main file>,
                "skill_name": <skill name>,
                "version": <version>,
                "additional_directories": [<additional directories>],
                "description": <description>,
                "language_dict": {<entry>: <text>}
                "license": <license>,
                "required_python3_packages": [<python3 packages>]}
        example: {"activate_phrases": {"start test": "test_method_start"}},
                "author": "blueShard",
                "language_locales": ["en_US"],
                "main_file": "test.py",
                "skill_name": "text_skill",
                "version": "1.0.0",
                "additional_directories": ["test_directory"],
                "description": "A simple skill to test the function 'get_skill_infos",
                "language_dict": {"test_func": "The test was successful"},
                "license": "MPL-2.0",
                "required_python3_packages": ["aionlib"]}

    :since: 0.1.0
    """
    try:
        from .utils import BaseXMLReader
    except ImportError:
        from utils import BaseXMLReader

    from ast import literal_eval
    skill_reader = BaseXMLReader(skills_file)
    return_dict = {"skill_name": skill_name}
    for value_list in skill_reader.get_infos("<all>").values():
        for skill in value_list:
            try:
                if skill["parent"]["tag"] == skill_name:
                    try:
                        return_dict[skill["tag"]] = literal_eval(skill["text"])
                    except (EOFError, SyntaxError, ValueError):
                        return_dict[skill["tag"]] = skill["text"]
            except KeyError:
                pass
    return return_dict


def remove_skill(skill_name: str) -> None:
    """
    removes given skill

    :param skill_name: str
        name of the skill you want to remove
        syntax: <skill name>
        example: "test"
    :return: None

    :since: 0.1.0
    """
    try:
        from .acph import delete_acph
        from .language import language_directory, delete_entry
        from .utils import BaseXMLReader, BaseXMLWriter
    except ImportError:
        from acph import delete_acph
        from language import language_directory, delete_entry
        from utils import BaseXMLReader, BaseXMLWriter

    from os import remove as os_remove
    from shutil import rmtree
    skill_infos = get_skill_infos(skill_name)
    os_remove(skills_path + "/" + skill_infos["main_file"])
    for dir in skill_infos["additional_directories"]:
        rmtree(skills_path + "/" + dir)
    for language in skill_infos["language_locales"]:
        delete_acph(language, [acph_dict["activate_phrase"] for acph_dict in skill_infos["activate_phrases"]])
        delete_entry(language, skill_name, entry_list=[key.replace(" ", "_") for key in skill_infos["language_dict"]])
    remove_xml = BaseXMLWriter(skills_file)
    remove_xml.remove("<root>", skill_name)
    remove_xml.write()
