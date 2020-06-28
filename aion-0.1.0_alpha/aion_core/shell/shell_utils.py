#!/usr/bin/python3

import sys
from glob import glob

sys.path.insert(1, glob("/usr/local/aion-*/aion_core/")[0])

import utils as atils


class AionShellError:
    """
    base class for errors while using the 'aion' shell command (for the exact identification of the error)
    """

    def __init__(self, errormsg: str, errno: str = "00000") -> None:
        """
        the error 'function'

        :param errormsg: str
            message that should be printed out
            syntax: <error message>
            example: "An example error occured"
        :param errno: str
            error number
            syntax: <error number>
            example: "11112"
        :return: None

        :since: 0.1.0
        """
        from colorama import Fore

        print(Fore.RED + "AionShellError: [Errno " + str(errno) + "]: " + str(errormsg) + Fore.RESET)


def arglen_check(arg_list: list, arg_len: int, max_arg_len: int = None) -> None:
    """
    checks if the length of a list is equal to a given length

    :param arg_list: list
        list you want to check if the length is equal to the given length
        syntax: [<list content>]
        example: ["example1", "example2"]
    :param arg_len: int
        length you want to check
        syntax: <length>
        example: 2
    :param max_arg_len: int
        if not None, it checks if the arg list length is between 'arg_len' and 'max_arg_len
        syntax: <max length>
        example: 4
    :return: None

    :since: 0.1.0
    """
    if max_arg_len is None:
        max_arg_len = arg_len
    if len(arg_list) < arg_len or len(arg_list) > max_arg_len:
        from colorama import Fore
        if arg_len == max_arg_len:
            if arg_len == 1:
                print(Fore.RED + "Expected 1 argument, got " + str(len(arg_list)) + " (" + ", ".join(arg_list) + "). Type 'aion help' for help" + Fore.RESET)
            else:
                print(Fore.RED + "Expected " + str(arg_len) + " arguments, got " + str(len(arg_list)) + " (" + ", ".join(arg_list) + "). Type 'aion help' for help" + Fore.RESET)
        else:
            print(Fore.RED + "Expected " + str(arg_len) + " to " + str(max_arg_len) + " arguments, got " + str(len(arg_list)) + " (" + ", ".join(arg_list) + "). Type 'aion help' for help" + Fore.RESET)
        exit(-1)


def which_package(package: str, input_sentence: str) -> int:
    """
    if a user want to uninstall (or something else) a skill or plugin and there are more than one plugin / skill with this name, this function get called

    :param package: str
        name of the package
        syntax: <package name>
        example: "test_package

    :param input_sentence: str
        sentence the user should be asked for input
        syntax: <input sentence>
        example: "Type in the number of your package type: "
    :return: int
        returns the type of the package (0 = skill; 1 = run after plugin; 2 = run before plugin)
        syntax: <package type>
        example: 2

    :since: 0.1.0
    """
    from plugin import get_all_run_after_plugins, get_all_run_before_plugins
    from skill import get_all_skills

    in_package = []

    if package in get_all_skills():
        in_package.append("Skill: " + str(len(in_package)))
    else:
        for plugin in get_all_run_after_plugins().values():
            if package in plugin:
                in_package.append("Run after plugin: " + str(len(in_package)))

        for plugin in get_all_run_before_plugins().values():
            if package in plugin:
                in_package.append("Run before plugin: " + str(len(in_package)))

        if len(in_package) == 0:
            return -1
        elif len(in_package) == 1:
            choose = 0
        else:
            for pa in in_package:
                print(pa)
            print("Found package '" + str(package) + "' multiple times")
            while True:
                input_choose = input(input_sentence)
                if str(input_choose) not in [str(l) for l in range(len(in_package))]:
                    print("Your number must be in " + ", ".join([str(l) for l in range(len(in_package))]))
                else:
                    choose = input_choose
                    break

        if in_package[choose].startswith("Skill"):
            return 0
        elif in_package[choose].startswith("Run after"):
            return 1
        elif in_package[choose].startswith("Run before"):
            return 2


def is_aion_running(command: str) -> None:
    """
    checks if aion is running

    :param command: str
        command that the user has typed in
        syntax: <command>
        example: "pid"
    :return: None

    :since: 0.1.0
    """
    import variable
    from ast import literal_eval
    from colorama import Fore
    if literal_eval(variable.Variable().get_value(variable.IS_AION_RUNNING)) is False:
        print(Fore.RED + command + " can only used if aion is running. Type 'aion run' or 'aion start' to start aion" + Fore.RESET)
        exit(-1)


def must_be_sudo() -> None:
    """
    checks if the user is root and if not it prints an warning message

    :return: None

    :since: 0.1.0
    """
    from colorama import Fore
    if atils.is_root() is False:
        print(Fore.RED + "to execute the command, aion must be run as sudo" + Fore.RESET)
        exit(-1)


def yesno(question: str) -> bool:
    """
    asks a yes no question

    :param question: str
        question you want to ask
        syntax: <question>
        example: "Execute test command? (y/n): "
    :return: bool
        returns if the user entered y / yes (True) or n / no (False)
        syntax: <boolean>
        example: True

    :since: 0.1.0
    """
    while True:
        yn = input(question)
        if yn.lower().strip() == "y" or yn.lower().strip() == "yes":
            return True
        elif yn.lower().strip() == "n" or yn.lower().strip() == "no":
            return False
        else:
            print("Please choose 'y' or 'n'")


class Install:

    """
    base class for installation
    """

    @staticmethod
    def aion() -> None:
        """
        installs aion

        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from os import system
        from shutil import rmtree
        system("git clone https://github.com/blueShard/aion_project /tmp/aion_project")
        system("bash /tmp/aion_project/install.sh")
        rmtree("/tmp/aion_project", ignore_errors=True)

    @staticmethod
    def plugin_from_aion_file(fname: str) -> None:
        """
        installs a plugin from a 'plugin.aion' file

        :param fname: str
            path of the file
            syntax: <filename>
            example: "/home/pi/test_plugin/plugin.aion"
        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from plugin import execute_aion_file_type_plugin
        execute_aion_file_type_plugin(fname)

    @staticmethod
    def plugin_from_plugin_file(fname: str) -> None:
        """
        installs a plugin from a '.plugin' package

        :param fname: str
            path of the file
            syntax: <filename>
            example: "/home/pi/test_plugin/test.plugin"
        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from plugin import execute_plugin_file
        execute_plugin_file(fname)

    @staticmethod
    def skill_from_aion_file(fname: str) -> None:
        """
        installs a skill from a 'skill.aion' file

        :param fname: str
            path of the file
            syntax: <filename>
            example: "/home/pi/test_skill/skill.aion"
        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from skill import execute_aion_file_type_skill
        execute_aion_file_type_skill(fname)

    @staticmethod
    def skill_from_skill_file(fname: str) -> None:
        """
        installs a skill from a '.skill' package

        :param fname: str
            path of the file
            syntax: <filename>
            example: "/home/pi/test_skill/test.skill"
        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from skill import execute_skill_file
        execute_skill_file(fname)

    @staticmethod
    def respeaker(compatibility_mode: bool = False) -> None:
        """
        installs respeaker

        :param compatibility_mode:
            installs an old kernel version which is definitely compatible with respeaker
            (the current version may contain patches etc. which make respeaker not work properly anymore and to which the developers of respeaker have to adapt the software first)
            syntax: <boolean>
            example: False
        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from os import system
        from shutil import copy, rmtree
        system("git clone https://github.com/respeaker/seeed-voicecard.git /tmp/seeed-voicecard")
        copy("/tmp/seeed-voicecard/uninstall.sh", atils.aion_path + "/etc/respeaker_uninstall.sh")
        if compatibility_mode:
            system("cd /tmp/seeed-voicecard/; ./install.sh --compat-kernel")
        else:
            system("cd /tmp/seeed-voicecard/; ./install.sh")
        system("amixer cset numid=3 2")
        rmtree("/tmp/seeed-voicecard", ignore_errors=True)


class Pack:

    """
    base class for packing plugin or skill directories to '.plugin' or '.skill' packages
    """

    @staticmethod
    def skill(directory: str) -> None:
        """
        creates a skill package from given directory

        :param directory: str
            path of the directory
            syntax: <filename>
            example: "/home/pi/test_skill.skill"
        :return: None

        :since: 0.1.0
        """
        from skill import create_skill_package

        create_skill_package(directory)

    @staticmethod
    def plugin(directory: str) -> None:
        """
        creates a plugin package from given directory

        :param directory: str
            path of the directory
            syntax: <filename>
            example: "/home/pi/test_plugin.plugin"
        :return: None

        :since: 0.1.0
        """
        from plugin import create_plugin_package

        create_plugin_package(directory)


class UnRem:  # this class name combine the word uninstall and remove

    @staticmethod
    def aion(personal_data: bool = False) -> None:
        """
        deletes aion

        :param personal_data: bool
            checks if all personal data should be deleted as well
            syntax: <boolean>
            example: True
        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from glob import glob
        from os import system
        if personal_data is True:
            system("bash " + glob("/usr/local/aion-*/etc/uninstall.sh")[0] + " --all")
        else:
            system("bash " + glob("/usr/local/aion-*/etc/uninstall.sh")[0])

    @staticmethod
    def aionlib() -> None:
        """
        uninstalls aionlib

        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from os import system
        system("yes | pip3 uninstall aionlib")

    @staticmethod
    def run_after_plugin(name: str) -> None:
        """
        uninstalls a run after plugin

        :param name: str
            name of the run after plugin
            syntax: <run after plugin>
            example: "test_run_after_plugin"
        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from plugin import RUN_AFTER, remove_plugin
        remove_plugin(name, RUN_AFTER)

    @staticmethod
    def run_before_plugin(name: str) -> None:
        """
        uninstalls a run before plugin

        :param name: str
            name of the run before plugin
            syntax: <run before plugin>
            example: "test_run_before_plugin"
        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from plugin import RUN_BEFORE, remove_plugin
        remove_plugin(name, RUN_BEFORE)

    @staticmethod
    def skill(name: str) -> None:
        """
        uninstalls a skill

        :param name: str
            name of the skill
            syntax: <skill>
            example: "test_skill"
        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from skill import remove_skill
        remove_skill(name)

    @staticmethod
    def respeaker() -> None:
        """
        uninstalls respeaker (if installed)

        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from os import path, system
        if path.isfile(atils.aion_path + "/etc/respeaker_uninstall.sh") is False:
            raise FileNotFoundError("can't find file '" + atils.aion_path + "/etc/respeaker_uninstall.sh' to uninstall respeaker")
        else:
            system("bash " + atils.aion_path + "/etc/respeaker_uninstall.sh")


class Update:

    @staticmethod
    def aion() -> None:
        """
        updates aion

        :return: None

        :since: 0.1.0
        """
        from colorama import Fore
        print(Fore.RED + "The update command for aion isn't created yet" + Fore.RESET)

    @staticmethod
    def aionlib() -> None:
        """
        updates aionlib

        :return: None

        :since: 0.1.0
        """
        must_be_sudo()
        from os import system
        system("yes | pip3 install --upgrade aionlib")

    @staticmethod
    def run_after_plugin(name: str) -> None:
        """
        updates a run after plugin

        :param name: str
            name of the plugin
            syntax: <plugin name>
            example: "test_run_after_plugin"
        :return: None

        :since: 0.1.0
        """
        from colorama import Fore
        print(Fore.RED + "The update command for 'run_after_plugin' isn't created yet")

    @staticmethod
    def run_before_plugin(name: str) -> None:
        """
        updates a run before plugin

        :param name: str
            name of the run before plugin
            syntax: <plugin name>
            example: "test_run_before_plugin"
        :return: None

        :since: 0.1.0
        """
        from colorama import Fore
        print(Fore.RED + "The update command for 'run_before_plugin' isn't created yet")

    @staticmethod
    def skill(name: str) -> None:
        """
        updates a skill

        :param name: str
            name if the skill
            syntax: <skill name>
            example: "test_skill"
        :return: None

        :since: 0.1.0
        """
        from colorama import Fore
        print(Fore.RED + "The update command for 'skill' isn't created yet")


class Version:

    @staticmethod
    def aion() -> None:
        """
        prints the version of 'aion'

        :return: None

        :since: 0.1.0
        """
        from glob import glob
        print("".join(glob("/usr/local/aion-*").remove("/usr/local/aion-")))

    @staticmethod
    def aionlib() -> None:
        """
        prints the version of aionlib (if installed)

        :return: None

        :since: 0.1.0
        """
        try:
            from aionlib import __version__ as aionlib_version
            print(aionlib_version)
        except ImportError:
            print("'aionlib' isn't installed. To install aionlib, type 'sudo pip3 install aionlib'")

    @staticmethod
    def run_after_plugin(name: str) -> None:
        """
        prints the version of a run after plugin

        :param name: str
            name of the plugin
            syntax: <plugin name>
            example: "test_run_after_plugin"
        :return: None

        :since: 0.1.0
        """
        from plugin import get_run_after_plugin_infos
        for key, item in get_run_after_plugin_infos(name):
            if key == "version":
                print(item)
                break

    @staticmethod
    def run_before_plugin(name: str) -> None:
        """
        prints the version of a run before plugin

        :param name: str
            name of the plugin
            syntax: <plugin name>
            example: "test_run_before_plugin"
        :return: None

        :since: 0.1.0
        """
        from plugin import get_run_before_plugin_infos
        for key, item in get_run_before_plugin_infos(name):
            if key == "version":
                print(item)
                break

    @staticmethod
    def skill(name: str) -> None:
        """
        prints the version of a skill

        :param name: str
            name of the skill
            syntax: <plugin name>
            example: "test_skill"
        :return: None

        :since: 0.1.0
        """
        from skill import get_skill_infos
        for key, item in get_skill_infos(name):
            if key == "version":
                print(item)
                break
