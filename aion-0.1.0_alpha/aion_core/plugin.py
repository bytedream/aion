#!/usr/bin/python3

try:
    from .utils import aion_data_path as _aion_data_path, BaseXMLReader as _BaseXMLReader
except ImportError:
    from utils import aion_data_path as _aion_data_path, BaseXMLReader as _BaseXMLReader


RUN_AFTER = "run_after"
RUN_BEFORE = "run_after"


run_after_path = _aion_data_path + "/plugins/run_after"
run_before_path = _aion_data_path + "/plugins/run_before"

run_after_file = _aion_data_path + "/plugins/run_after/run_after.xml"
run_before_file = _aion_data_path + "/plugins/run_before/run_before.xml"


class RunAfter:
    """
    base class to create custom 'run_after' plugins

    :since: 0.1.0
    """

    def __init__(self, activate_phrase: str, speech_input: str) -> None:
        """
        makes the variables available for all class functions

        :param activate_phrase: str
            activate phrase from which this class was called
            syntax: <activate phrase>
            example: "start plugin test"
        :param speech_input: str
            input that the user has spoken in
            syntax: <speech input>
            example: "start plugin test"
        :return: None

        :since: 0.1.0
        """
        self.activate_phrase = activate_phrase
        self.speech_input = speech_input

    def main(self) -> None:
        """
        gets called if the class get called from the 'run_after_plugin' plugin of the 'Skill' class

        :return: None

        :since: 0.1.0
        """
        pass


class RunBefore:
    """
    base class to create custom 'run_before' plugins

    :since: 0.1.0
    """

    def __init__(self, activate_phrase: str, speech_input: str) -> None:
        """
        makes the variables available for all class functions

        :param activate_phrase: str
            activate phrase from which this class was called
            syntax: <activate phrase>
            example: "start plugin test"
        :param speech_input: str
            input that the user has spoken in
            syntax: <speech input>
            example: "start plugin test"
        :return: None

        :since: 0.1.0
        """
        self.activate_phrase = activate_phrase
        self.speech_input = speech_input

    def main(self) -> None:
        """
        gets called if the class get called from the 'run_before_plugin' function of the 'Skill' class

        :return: None

        :since: 0.1.0
        """
        pass


def create_run_after_plugin_file(author: str,
                                 plugin_name: str,
                                 main_file: str,
                                 skill: str,
                                 plugin_methods: dict,
                                 version: str,
                                 additional_directories: list = [],
                                 description: str = "",
                                 language_locales: list = [],
                                 language_dict: dict = {},
                                 license: str = "",
                                 required_python3_packages: list = []) -> None:
    """
    creates a file from which a 'run_after' plugin can be installed

    :param author: str
        name of the author from the plugin
        syntax: <author name>
        example: "blueShard"
    :param main_file: str
        file name of file where all plugin methods are defined
        syntax: <file name>
        example: "test.py"
        NOTE: the file must be in the same directory as the file from which 'create_run_after_plugin_file' is being executed
    :param plugin_name: str
        root name of the plugin you create
        syntax: <plugin name>
        example: "text_plugin"
    :param skill: str
        name of the skill you want to add the 'run_before' plugin
        syntax: <skill name>
        example: "Play"
        NOTE: be case-sensitive!
    :param plugin_methods: dict
        dictionary of plugin pseudonym with plugin method you want to add to given 'skill'
        syntax: {"<plugin pseudonym>": <plugin methods>}
        example: ["test_plugin_run_test_2": "TestPlugin"]
        NOTE: be case-sensitive!
        NOTE2: the plugins pseudonyms are only pseudonyms for the given methods
        NOTE3: you can't remove individual plugins via the 'aion' command line command
    :param version: str
        version (number) of your plugin
        syntax: <version>
        example: "1.0.0"
    :param additional_directories: list, optional
        list of additional directories your main file needs for execution
        syntax: [<additional directories>]
        example: ["test_directory"]
        NOTE: the directories must be in the same directory as the file from which 'create_run_after_plugin_file' is being executed
    :param description: str, optional
        description of your plugin
        syntax: <description>
        example: "A simple plugin to test the method 'create_run_after_plugin_file'"
    :param language_locales: list
        list of language locales for which the 'language_dict' should be stored
        syntax: [<language locale>]
        example: ["en_US"]
    :param language_dict: dict, optional
        dictionary of messages which are saved in (from argument 'language_locales' given) '.lng' files
        syntax: {<entry>, <text>}
        example: {"test_entry": "The test was successful"}
        NOTE: the method name should be included in the entry for legibility
        NOTE2: for more infos about language ('.lng') files, see file 'language.py'
    :param license: str, optional
        license of the plugin
        syntax: <license>
        example: "MPL-2.0"
    :param required_python3_packages: list, optional
        list of python3 packages your plugin needs for correct execution
        syntax: [<python3 package>]
        example: ["aionlib"]
    :return: None

    :since: 0.1.0
    """
    _create_befater_plugin_file("run_after",
                                author,
                                plugin_name,
                                main_file,
                                skill,
                                plugin_methods,
                                version,
                                additional_directories,
                                description,
                                language_locales,
                                language_dict,
                                license,
                                required_python3_packages)


def create_run_before_plugin_file(author: str,
                                  plugin_name: str,
                                  main_file: str,
                                  skill: str,
                                  plugin_methods: dict,
                                  version: str,
                                  additional_directories: list = [],
                                  description: str = "",
                                  language_locales: list = [],
                                  language_dict: dict = {},
                                  license: str = "",
                                  required_python3_packages: list = []) -> None:
    """
    creates a file from which a 'run_before' plugin can be installed

    :param author: str
        name of the author from the plugin
        syntax: <author name>
        example: "blueShard"
    :param main_file: str
        file name of file where all plugin methods are defined
        syntax: <file name>
        example: "test.py"
        NOTE: the file must be in the same directory as the file from which 'create_run_before_plugin_file' is being executed
    :param plugin_name: str
        root name of the plugins you create
        syntax: <plugin name>
        example: "text_plugin"
    :param skill: str
        name of the skill you want to add the 'run_before' plugin
        syntax: <skill name>
        example: "Play"
        NOTE: be case-sensitive!
    :param plugin_methods: dict
        dictionary of plugin pseudonym with plugin method you want to add to given 'skill'
        syntax: {"<plugin pseudonyms>": <plugin methods>}
        example: ["test_plugin_run_test_2": "TestPlugin"]
        NOTE: be case-sensitive!
        NOTE2: the plugins pseudonyms are only pseudonyms for the given methods
        NOTE3: you can't remove individual plugins via the 'aion' command line command
    :param plugin_name: str
        name of the plugin you create
        syntax: <plugin name>
        example: "text_plugin"
    :param version: str
        version (number) of your plugin
        syntax: <version>
        example: "1.0.0"
    :param additional_directories: list, optional
        list of additional directories your main file needs for execution
        syntax: [<additional directories>]
        example: ["test_directory"]
        NOTE: the directories must be in the same directory as the file from which 'create_run_before_plugin_file' is being executed
    :param description: str, optional
        description of your plugin
        syntax: <description>
        example: "A simple plugin to test the method 'create_run_after_plugin_file'"
    :param language_locales: list
        list of language locales for which the 'language_dict' should be stored
        syntax: [<language locale>]
        example: ["en_US"]
    :param language_dict: dict, optional
        dictionary of messages which are saved in (from argument 'language_locales' given) '.lng' files
        syntax: {<entry>, <text>}
        example: {"test_entry": "The test was successful"}
        NOTE: the method name should be included in the entry for legibility
        NOTE2: for more infos about language ('.lng') files, see file 'language.py'
    :param license: str, optional
        license of the plugin
        syntax: <license>
        example: "MPL-2.0"
    :param required_python3_packages: list, optional
        list of python3 packages your plugin needs for correct execution
        syntax: [<python3 package>]
        example: ["aionlib"]
    :return: None

    :since: 0.1.0
    """
    _create_befater_plugin_file("run_before",
                                author,
                                plugin_name,
                                main_file,
                                skill,
                                plugin_methods,
                                version,
                                additional_directories,
                                description,
                                language_locales,
                                language_dict,
                                license,
                                required_python3_packages)


def create_plugin_package(dir_name: str) -> None:
    """
    creates a stand alone file ('.plugin') from given directory

    :param dir_name: str
        directory name of the directory from which you want to create a '.plugin' file
        syntax: <directory name>
        example: "/home/pi/test/"
    :return: None

    :note: 'plugin.aion' file must be in the given directory (see 'create_run_after_plugin_file' / 'create_run_before_plugin_file' to create a 'plugin.aion' file)

    :since: 0.1.0
    """
    try:
        from ._error_codes import plugin_aion_plugin_file_not_found, plugin_to_much_aion_files
    except ImportError:
        from _error_codes import plugin_aion_plugin_file_not_found, plugin_to_much_aion_files

    from os import listdir, mkdir, rename
    from os.path import isdir
    from random import sample
    from shutil import make_archive, rmtree

    if isdir(dir_name) is False:
        raise NotADirectoryError("couldn't find the directory '" + dir_name + "'")

    name = ""
    file_num = 0
    for file in listdir(dir_name):
        if file.endswith(".aion"):
            file_num += 1
            name = "".join(file.split(".aion")[0])
    if file_num == 0:
        raise FileNotFoundError("Errno: " + plugin_aion_plugin_file_not_found + " - Couldn't find .aion file in " + dir_name + ". To create one use the 'create_plugin_file' function in aionlib.skill")
    elif file_num > 1:
        raise FileExistsError("Errno: " + plugin_to_much_aion_files + " - Expected one .aion file in " + dir_name + ", got " + str(file_num))

    plugin_dir_name = "plugin_" + name + "".join([str(num) for num in sample(range(1, 10), 5)])
    mkdir(plugin_dir_name)

    make_archive(name + ".plugin", "zip", plugin_dir_name)
    rename(plugin_dir_name + ".plugin.zip", plugin_dir_name + ".plugin")

    rmtree(plugin_dir_name)


def execute_aion_file_type_plugin(fname: str) -> None:
    """
    installs custom plugin from '<file name>.aion'

    :param fname: str
        file name of the '.aion' file
        syntax: <file name>
        example: "/home/pi/plugin.aion"
    :return: None

    :since: 0.1.0
    """
    try:
        from ._errors import plugin_couldnt_find_key, plugin_couldnt_find_plugin_type, plugin_illegal_run_after_pseudonym, plugin_run_after_pseudonym_already_exist,\
            plugin_illegal_run_before_pseudonym, plugin_run_before_pseudonym_already_exist, plugin_file_doesnt_exist_in_setup_dir, plugin_directory_doesnt_exist_in_setup_dir,\
            plugin_run_after_additional_directories_already_exist, plugin_run_before_additional_directories_already_exist, plugin_python3_module_not_found
        from .acph import add_acph
        from .language import add_entry, language_directory
        from .utils import remove_space, BaseXMLReader, BaseXMLWriter
    except ImportError:
        from _error_codes import plugin_couldnt_find_key, plugin_couldnt_find_plugin_type, plugin_illegal_run_after_pseudonym, plugin_run_after_pseudonym_already_exist,\
            plugin_illegal_run_before_pseudonym, plugin_run_before_pseudonym_already_exist, plugin_file_doesnt_exist_in_setup_dir, plugin_directory_doesnt_exist_in_setup_dir,\
            plugin_run_after_additional_directories_already_exist, plugin_run_before_additional_directories_already_exist, plugin_python3_module_not_found
        from acph import add_acph
        from language import add_entry, language_directory
        from utils import remove_space, BaseXMLReader, BaseXMLWriter

    from ast import literal_eval
    from importlib import import_module
    from os import listdir, path
    from shutil import copy, copytree
    from subprocess import call
    setup_dict = {}
    setup_dir = path.dirname(path.abspath(fname))

    plugin_type = ""
    is_skill = True

    for line in open(fname, "r"):
        if line.startswith("#"):
            no_space_line = remove_space(line, "")
            if no_space_line == "#type:run_after_plugin":
                plugin_type = RUN_AFTER
            elif no_space_line == "#type:run_before_plugin":
                plugin_type = RUN_BEFORE
            continue

        setup_dict[line.split("=")[0].strip()] = line.split("=")[1].strip()
    try:
        author = setup_dict["author"]
        main_file = setup_dict["main_file"]
        plugin_name = setup_dict["plugin_name"]
        skill = setup_dict["skill"]
        plugin_methods = literal_eval(setup_dict["plugin_methods"])
        version = setup_dict["version"]

        additional_directories = literal_eval(setup_dict["additional_directories"])
        description = setup_dict["description"]
        language_locales = literal_eval(setup_dict["language_locales"])
        language_dict = literal_eval(setup_dict["language_dict"])
        license = setup_dict["license"]
        required_python3_packages = literal_eval(setup_dict["required_python3_packages"])
    except KeyError as error:
        raise KeyError("Errno: " + plugin_couldnt_find_key + " - Couldn't find key " + str(error) + " in " + fname)

    if plugin_type != RUN_AFTER or plugin_type != RUN_BEFORE:
        raise NameError("Errno: " + plugin_couldnt_find_plugin_type + " - Couldn't find plugin type ('RUN_AFTER' or 'RUN_BEFORE') in " + fname)

    # ----- #

    if plugin_type == RUN_AFTER:
        for pseudonym in plugin_methods:
            if pseudonym == "run_after":
                raise NameError("Errno: " + plugin_illegal_run_after_pseudonym + " - Illegal name '" + pseudonym + "' in " + str(plugin_methods))
            try:
                if pseudonym in get_all_run_after_plugins()[skill]:
                    raise NameError("Errno: " + plugin_run_before_pseudonym_already_exist + " - The plugin pseudonym " + plugin_name + " already exist")
            except KeyError:
                is_skill = False
                pass

    elif plugin_type == RUN_BEFORE:
        for pseudonym in plugin_methods:
            if pseudonym == "run_before":
                raise NameError("Errno: " + plugin_illegal_run_before_pseudonym + " - Illegal name '" + pseudonym + "' in " + str(plugin_methods))
            try:
                if pseudonym in get_all_run_before_plugins()[skill]:
                    raise NameError("Errno: " + plugin_run_after_pseudonym_already_exist + " - The plugin pseudonym " + plugin_name + " already exist")
            except KeyError:
                is_skill = False
                pass

    if path.isfile(setup_dir + "/" + main_file) is False:
        raise FileNotFoundError("Errno: " + plugin_file_doesnt_exist_in_setup_dir + " - The file " + main_file + " doesn't exist in setup dir (" + setup_dir + ")")

    for directory in additional_directories:
        if path.isdir(setup_dir + "/" + directory) is False:
            raise NotADirectoryError("Errno: " + plugin_directory_doesnt_exist_in_setup_dir + " - The directory " + directory + " doesn't exist in setup dir (" + setup_dir + ")")
        if plugin_type == RUN_AFTER:
            if directory in listdir(run_after_path):
                raise IsADirectoryError("Errno: " + plugin_run_after_additional_directories_already_exist + " - The directory " + directory + " already exist in " + run_after_path)
        elif plugin_type == RUN_BEFORE:
            if directory in listdir(run_before_path):
                raise IsADirectoryError("Errno: " + plugin_run_before_additional_directories_already_exist + " - The directory " + directory + " already exist in " + run_before_path)

    # ----- #

    for package in required_python3_packages:
        call("pip3 install " + package, shell=True)
        try:
            import_module(package)
        except ModuleNotFoundError:
            raise ModuleNotFoundError("Errno: " + plugin_python3_module_not_found + " - Couldn't install the required python3 package '" + package + "'")

    dat_writer = None

    if plugin_type == RUN_AFTER:
        copy(main_file, run_after_path + "/" + main_file)

        for directory in additional_directories:
            copytree(directory, run_after_path + "/" + directory)

        for language in language_locales:
            add_entry(language, plugin_name, language_dict)

        dat_writer = BaseXMLWriter(run_after_file)

        if is_skill is False:
            dat_writer.add("run_after", skill, type="skill")
            dat_writer.write()

    elif plugin_type == RUN_BEFORE:
        copy(main_file, run_after_path + "/" + main_file)

        for directory in additional_directories:
            copytree(directory, run_after_path + "/" + directory)

        for language in language_locales:
            add_entry(language, plugin_name, language_dict)

        dat_writer = BaseXMLWriter(run_before_file)

        if is_skill is False:
            dat_writer.add("run_before", skill, type="skill")
            dat_writer.write()

    for pseudonym, method in plugin_methods.values():
        dat_writer.add(skill, str(pseudonym), parent_attrib={"type": "skill"}, method=method, root_plugin=plugin_name)
        dat_writer.add(str(pseudonym), "additional_directories", str(additional_directories))
        dat_writer.add(str(pseudonym), "author", str(author))
        dat_writer.add(str(pseudonym), "description", str(description))
        dat_writer.add(str(pseudonym), "language_dict", str(language_dict))
        dat_writer.add(str(pseudonym), "language_locales", str(language_locales))
        dat_writer.add(str(pseudonym), "license", str(license))
        dat_writer.add(str(pseudonym), "main_file", str(main_file))
        dat_writer.add(str(pseudonym), "required_python3_packages", str(required_python3_packages))
        dat_writer.add(str(pseudonym), "version", str(version))
    dat_writer.write()


def execute_plugin_file(fname: str) -> None:
    """
    executes a '<name>.plugin' file for installing custom plugins

    :param fname: str
        file name of the '.plugin' file
        syntax: <fname>
        example: "/home/pi/test.plugin"
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import plugin_couldnt_find_plugin_dot_aion
    except ImportError:
        from _error_codes import plugin_couldnt_find_plugin_dot_aion

    from glob import glob
    from os.path import isfile
    from zipfile import ZipFile
    with ZipFile(fname, "r") as zipfile:
        zipfile.extractall("/tmp")
        zipfile.close()
    if isfile(glob("/tmp/plugin_*/plugin.aion")[0]) is False:
        raise FileNotFoundError("Errno: " + plugin_couldnt_find_plugin_dot_aion + "couldn't find 'plugin.aion' in " + fname)
    else:
        execute_aion_file_type_plugin(glob("/tmp/plugin_*/plugin.aion")[0])


def get_all_run_after_plugins() -> dict:
    """
    get all installed 'run_after' plugins + infos

    :return: dict
        returns dict of all plugins + infos

    :since: 0.1.0
    """
    try:
        from .utils import is_dict_in_dict
    except ImportError:
        from utils import is_dict_in_dict

    run_after = {}

    for value in _BaseXMLReader(run_after_file).get_infos("<all>").values():
        for child in value:
            attrib = child["attrib"]
            parent_tag = child["parent"]["tag"]
            parent_attrib = child["parent"]["attrib"]
            if is_dict_in_dict({"type": "skill"}, parent_attrib):
                try:
                    run_after[parent_tag][child["tag"]] = {"method": attrib["method"], "root_plugin": attrib["root_plugin"]}
                except KeyError:
                    run_after[parent_tag] = {}
            else:
                for skill in run_after.values():
                    for plugin in skill:
                        if plugin == parent_tag:
                            run_after[skill][plugin][child["tag"]] = child["text"]
                            break

    return run_after


def get_all_run_before_plugins() -> dict:
    """
    get all installed 'run_before' plugins + infos

    :return: dict
        returns dict of all plugins + infos

    :since: 0.1.0
    """
    try:
        from .utils import is_dict_in_dict
    except ImportError:
        from utils import is_dict_in_dict

    run_before = {}

    for value in _BaseXMLReader(run_before_file).get_infos("<all>").values():
        for child in value:
            attrib = child["attrib"]
            parent_tag = child["parent"]["tag"]
            parent_attrib = child["parent"]["attrib"]
            if is_dict_in_dict({"type": "skill"}, parent_attrib):
                try:
                    run_before[parent_tag][child["tag"]] = {"method": attrib["method"], "root_plugin": attrib["root_plugin"]}
                except KeyError:
                    run_before[parent_tag] = {}
            else:
                for skill in run_before.values():
                    for plugin in skill:
                        if plugin == parent_tag:
                            run_before[skill][plugin][child["tag"]] = child["text"]
                            break

    return run_before


def get_run_after_plugin_infos(plugin_name: str) -> dict:
    """
    returns infos about an given 'run_after' plugin

    :param plugin_name: str
        the name of the 'run_after' plugin
        syntax: <plugin name>
        example: "test_plugin"
    :return: dict
        returns a dictionary with infos of the 'run_after' plugin
        syntax: {"author": <author>,
                "main_file": <main file>,
                "plugin_root_name": <plugin root name>
                "plugin_name": <plugin name>,
                "plugin_method": <plugin method>
                "version": <version>,
                "additional_directories": [<additional directories>],
                "description": <description>,
                "language_locales": [<language locales>],
                "language_dict": {<entry>: <text>}
                "license": <license>,
                "required_python3_packages": [<python3 packages>]}
        example: {"author": "blueShard",
                "main_file": "test.py",
                "plugin_root_name:": "test_plugin"
                "plugin_name": "test_plugin_run_after",
                "plugin_method": "test_plugin_method"
                "version": "1.0.0",
                "additional_directories": ["test_directory"],
                "description": "A simple plugin to test the method 'get_run_after_plugin_infos",
                "language_locales": ["en_US"],
                "language_dict": {"test_method": "The test was successful"},
                "license": "MPL-2.0",
                "required_python3_packages": ["aionlib"]}

    :since: 0.1.0
    """
    for skill in get_all_run_after_plugins().values():
        for plugin, infos in skill.values():
            if plugin == plugin_name:
                return infos


def get_run_before_plugin_infos(plugin_name: str) -> dict:
    """
    returns infos about an given 'run_before' plugin

    :param plugin_name: str
        the name of the 'run_after' plugin
        syntax: <plugin name>
        example: "test_plugin"
    :return: dict
        returns a dictionary with infos of the 'run_after' plugin
        syntax: {"author": <author>,
                "main_file": <main file>,
                "plugin_root_name": <plugin root name>
                "plugin_name": <plugin name>,
                "plugin_method": <plugin method>
                "version": <version>,
                "additional_directories": [<additional directories>],
                "description": <description>,
                "language_locales": [<language locales>],
                "language_dict": {<entry>: <text>}
                "license": <license>,
                "required_python3_packages": [<python3 packages>]}
        example: {"author": "blueShard",
                "main_file": "test.py",
                "plugin_root_name:": "test_plugin"
                "plugin_name": "test_plugin_run_before",
                "plugin_method": "test_plugin_method"
                "version": "1.0.0",
                "additional_directories": ["test_directory"],
                "description": "A simple plugin to test the method 'get_run_before_plugin_infos",
                "language_locales": ["en_US"],
                "language_dict": {"test_method": "The test was successful"},
                "license": "MPL-2.0",
                "required_python3_packages": ["aionlib"]}

    :since: 0.1.0
    """
    for skill in get_all_run_before_plugins().values():
        for plugin, infos in skill.values():
            if plugin == plugin_name:
                return infos


def remove_plugin(plugin_name: str, plugin_type: (RUN_AFTER, RUN_BEFORE)) -> None:
    """
    removes given plugin

    :param plugin_name: str
        name of the plugin you want to remove
        syntax: <plugin name>
        example: "test"
    :param plugin_type: (RUN_AFTER, RUN_BEFORE)
        type of the plugin
        syntax: <plugin type>
        example: RUN_AFTER

    :since: 0.1.0
    """
    try:
        from .language import language_directory, delete_entry
        from .utils import BaseXMLReader, BaseXMLWriter
    except ImportError:
        from language import language_directory, delete_entry
        from utils import BaseXMLReader, BaseXMLWriter

    from ast import literal_eval
    from os import remove as remove
    from shutil import rmtree

    if plugin_type == RUN_AFTER:
        plugin_infos = get_run_after_plugin_infos(plugin_name)
        remove(run_after_path + "/" + plugin_infos["main_file"])
        for dir in plugin_infos["additional_directories"]:
            rmtree(run_after_path + "/" + dir)
        for language in plugin_infos["language_locales"]:
            delete_entry(language, plugin_name, entry_list=[key.replace(" ", "_") for key in literal_eval(plugin_infos["language_dict"])])
        remove_xml = BaseXMLWriter(run_after_file)
        remove_xml.remove(plugin_infos["method"], plugin_name)
        remove_xml.write()


def _create_befater_plugin_file(type: (RUN_AFTER, RUN_BEFORE),
                                author: str,
                                plugin_name: str,
                                main_file: str,
                                skill: str,
                                plugin_methods: dict,
                                version: str,
                                additional_directories: list = [],
                                description: str = "",
                                language_locales: list = [],
                                language_dict: dict = {},
                                license: str = "",
                                required_python3_packages: list = []) -> None:
    """
    creates a file from which a plugin can be installed

    :param type: (RUN_AFTER, RUN_BEFORE)
        type of the plugin
        syntax: <plugin type>
        example: RUN_AFTER
    :param author: str
        name of the author from the plugin
        syntax: <author name>
        example: "blueShard"
    :param main_file: str
        file name of file where all plugin methods are defined
        syntax: <file name>
        example: "test.py"
        NOTE: the file must be in the same directory as the file from which 'create_run_after_plugin_file' is being executed
    :param plugin_name: str
        root name of the plugin you create
        syntax: <plugin name>
        example: "text_plugin"
    :param skill: str
        name of the skill you want to add the 'run_before' plugin
        syntax: <skill name>
        example: "Play"
        NOTE: be case-sensitive!
    :param plugin_methods: dict
        dictionary of plugin pseudonym with plugin method you want to add to given 'skill'
        syntax: {"<plugin pseudonym>": <plugin methods>}
        example: ["test_plugin_run_test_2": "TestPlugin"]
        NOTE: be case-sensitive!
        NOTE2: the plugins pseudonyms are only pseudonyms for the given methods
        NOTE3: you can't remove individual plugins via the 'aion' command line command
    :param version: str
        version (number) of your plugin
        syntax: <version>
        example: "1.0.0"
    :param additional_directories: list, optional
        list of additional directories your main file needs for execution
        syntax: [<additional directories>]
        example: ["test_directory"]
        NOTE: the directories must be in the same directory as the file from which 'create_run_after_plugin_file' is being executed
    :param description: str, optional
        description of your plugin
        syntax: <description>
        example: "A simple plugin to test the method 'create_run_after_plugin_file'"
    :param language_locales: list
        list of language locales for which the 'language_dict' should be stored
        syntax: [<language locale>]
        example: ["en_US"]
    :param language_dict: dict, optional
        dictionary of messages which are saved in (from argument 'language_locales' given) '.lng' files
        syntax: {<entry>, <text>}
        example: {"test_entry": "The test was successful"}
        NOTE: the method name should be included in the entry for legibility
        NOTE2: for more infos about language ('.lng') files, see file 'language.py'
    :param license: str, optional
        license of the plugin
        syntax: <license>
        example: "MPL-2.0"
    :param required_python3_packages: list, optional
        list of python3 packages your plugin needs for correct execution
        syntax: [<python3 package>]
        example: ["aionlib"]
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import  plugin_author_must_be_str, plugin_plugin_name_must_be_str, plugin_main_file_must_be_str, plugin_main_file_not_found, plugin_main_file_name_must_be_plugin_name,\
            plugin_skill_must_be_dict, plugin_plugin_methods_must_be_dict, plugin_version_must_be_str, plugin_additional_directories_must_be_list_or_tuple,\
            plugin_couldnt_find_additional_directories_directory, plugin_description_must_be_str, plugin_language_locales_must_be_list_or_tuple, plugin_language_dict_must_be_dict,\
            plugin_language_dict_character_must_be_in_alphabet, plugin_license_must_be_str, plugin_required_python3_package_must_be_list_or_tuple
    except ImportError:
        from _error_codes import plugin_author_must_be_str, plugin_plugin_name_must_be_str, plugin_main_file_must_be_str, plugin_main_file_not_found, plugin_main_file_name_must_be_plugin_name,\
            plugin_skill_must_be_dict, plugin_plugin_methods_must_be_dict, plugin_version_must_be_str, plugin_additional_directories_must_be_list_or_tuple,\
            plugin_couldnt_find_additional_directories_directory, plugin_description_must_be_str, plugin_language_locales_must_be_list_or_tuple, plugin_language_dict_must_be_dict,\
            plugin_language_dict_character_must_be_in_alphabet, plugin_license_must_be_str, plugin_required_python3_package_must_be_list_or_tuple

    from os import getcwd, listdir

    write_dict = {}

    if isinstance(author, str) is False:
        raise TypeError("Errno: " + plugin_author_must_be_str + " - Argument 'author' must be str, got " + type(author).__name__)
    write_dict["author"] = author

    if isinstance(plugin_name, str) is False:
        raise TypeError("Errno: " + plugin_plugin_name_must_be_str + " - Argument 'plugin_name' must be str, got " + type(plugin_name).__name__)
    write_dict["plugin_name"] = plugin_name

    if isinstance(main_file, str) is False:
        raise TypeError("Errno: " + plugin_main_file_must_be_str + " - argument 'main_file' must be str, got " + type(author).__name__)
    if main_file not in listdir(getcwd()):
        raise FileNotFoundError("Errno: " + plugin_main_file_not_found + " - Couldn't find the file " + main_file + " in current directory")
    if main_file[:-3] == plugin_name is False:
        raise NameError("Errno: " + plugin_main_file_name_must_be_plugin_name + " - The file name from " + main_file + " must be same as the argument 'plugin_name' (" + plugin_name + ")")
    write_dict["main_file"] = main_file

    if isinstance(skill, str) is False:
        raise TypeError("Errno: " + plugin_skill_must_be_dict + " - Argument 'skill' must be dict, got " + type(plugin_methods).__name__)
    write_dict["skill"] = skill

    if isinstance(plugin_methods, dict) is False:
        raise TypeError("Errno: " + plugin_plugin_methods_must_be_dict + " - Argument 'plugin_methods' must be dict, got " + type(plugin_methods).__name__)
    write_dict["plugin_methods"] = plugin_methods

    if isinstance(version, str) is False:
        raise TypeError("Errno: " + plugin_version_must_be_str + " - Argument 'version' must be str, got " + type(version).__name__)
    write_dict["version"] = version

    # ----- #

    if isinstance(additional_directories, (list, tuple)) is False:
        raise TypeError("Errno: " + plugin_additional_directories_must_be_list_or_tuple + " - Argument 'additional_directories' must be list or tuple, got " + type(additional_directories).__name__)
    for directory in additional_directories:
        if directory not in listdir(getcwd()):
            raise NotADirectoryError("Errno: " + plugin_couldnt_find_additional_directories_directory + " - Couldn't find the directory " + directory + " in current directory")
    write_dict["additional_directories"] = additional_directories

    if isinstance(description, str) is False:
        raise TypeError("Errno: " + plugin_description_must_be_str+ " - Argument 'description' must be str, got " + type(description).__name__)
    write_dict["description"] = description

    if isinstance(language_locales, (list, tuple)) is False:
        raise TypeError("Errno: " + plugin_language_locales_must_be_list_or_tuple + " - Argument 'language_locales' must be list or tuple, got " + type(language_locales).__name__)
    write_dict["language_locales"] = language_locales

    if isinstance(language_dict, dict) is False:
        raise TypeError("Errno: " + plugin_language_locales_must_be_list_or_tuple + " - Argument 'language_dict' must be dict, got " + type(language_dict).__name__)
    for key in language_dict.keys():
        tmp_string = ""
        for char in key:
            if char == " ":
                char = "_"
            if char.lower() not in "abcdefghijklmnopqrstuvwxyz_":
                raise ValueError("Errno: " + plugin_language_dict_character_must_be_in_alphabet + " - Letter " + str(char) + " in " + str(key) + " must be in 'ABCDEFGHIJLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyz_'")
            tmp_string = tmp_string + char
        language_dict[tmp_string] = language_dict.pop(key)
    write_dict["language_dict"] = language_dict

    if isinstance(license, str) is False:
        raise TypeError("Errno: " + plugin_license_must_be_str + " - Argument 'license' must be str, got " + type(license).__name__)
    write_dict["license"] = license

    if isinstance(required_python3_packages, (list, tuple)) is False:
        raise TypeError("Errno: " + plugin_required_python3_package_must_be_list_or_tuple + " - Argument 'required_python3_packages' must be list or tuple, got " + type(required_python3_packages).__name__)
    write_dict["required_python3_packages"] = required_python3_packages

    # ----- #

    with open("plugin.aion", "w") as file:
        file.write("#type: " + type.lower() + "_plugin\n")
        for key, value in write_dict.items():
            file.write(key + " = " + str(value) + "\n")
        file.close()


def _run_befater_plugin(type: (RUN_AFTER, RUN_BEFORE), fname: str, plugin_name: str, activate_phrase: str, speech_input: str) -> None:
    """
    runs a plugin

    :param type: (RUN_AFTER, RUN_BEFORE)
        type of the plugin
        syntax: <plugin type>
        example: RUN_AFTER
    :param fname: str
        file path of the plugin file
        syntax: <filename>
        example: "/home/pi/test.py"
    :param plugin_name: str
        name of the plugin
        syntax: <plugin name>
        example: "TestPlugin"
    :param activate_phrase: str
        activate phrase, which calls the skill class to which the plugin belongs
        syntax: <activate phrase>
        example: "Start test plugin"
    :param speech_input: str
        speech input, which calls the skill class to which the plugin belongs
        syntax: <speech input>
        example: "Start test plugin"
    :return: None

    :since: 0.1.0
    """
    from sys import path
    path.insert(1, _aion_data_path + "/" + type.lower())
    exec("__import__('" + fname + "')." + plugin_name + "(" + activate_phrase + ", " + speech_input + ").main()")