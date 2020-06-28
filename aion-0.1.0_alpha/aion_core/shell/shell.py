#!/usr/bin/python3

from shell_utils import *

import sys

sys.path.insert(0, "..")


help = """
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
"""


def main():

    from argparse import ArgumentParser, RawTextHelpFormatter
    import os

    parser = ArgumentParser(description="Command line support for the 'aion' project", formatter_class=RawTextHelpFormatter, add_help=False)

    parser.add_argument("command", nargs="+")

    args = parser.parse_args()

    try:
        command = args.command[0].strip()

        if os.path.isfile(command):
            import __init__
            __init__.ExecuteAionFile(command)

        elif command == "help" or command == "-help" or command == "--help":
            print(help)

        elif command == "start" or command == "run":
            os.system("python3 " + atils.aion_path + "/main.py")

        elif command == "install":
            errno = "77227"
            arglen_check(args.command, 2)
            package = args.command[1]
            if package == "aion":
                must_be_sudo()
                Install.aion()
                print("Installed aion")
            elif package == "respeaker":
                must_be_sudo()
                Install.respeaker(yesno("Install in compatibility mode? (installs older kernel version)? (y/n): "))
                print("Installed respeaker")
            elif os.path.exists(package):
                if package.strip() == "skill.aion":
                    Install.skill_from_aion_file(package)
                elif package.strip() == "plugin.aion":
                    Install.plugin_from_aion_file(package)
                elif package.endswith(".skill"):
                    Install.skill_from_skill_file(package)
                elif package.endswith(".plugin"):
                    Install.plugin_from_plugin_file(package)
                else:
                    AionShellError(package + " is an unknowing skill / plugin. Type 'aion help' for help", errno)
            else:
                AionShellError(package + " is an unknowing skill / plugin. Type 'aion help' for help", errno)

        elif args.command in ["kill", "stop"]:  # kist
            arglen_check(args.command, 1)
            is_aion_running(command)
            import variable
            import signal
            avar = variable.Variable()
            os.kill(int(avar.get_value("AION_PID")), signal.SIGKILL)

        elif command == "load":
            arglen_check(args.command, 2, 3)
            import save as asave
            if len(args.command) == 3:
                asave.load_save(str(args.command[1]), str(args.command[2]))
            else:
                asave.load_save(str(args.command[1]))

        elif command == "pack":
            no_skill_plugin_file_errno = "27177"
            no_dir_errno = "27178"
            arglen_check(args.command, 2)
            dir = args.command[1]
            if os.path.isdir(dir):
                if os.path.isfile(dir + "/skill.aion"):
                    Pack.skill(dir)
                elif os.path.isfile(dir + "/plugin.aion"):
                    Pack.plugin(dir)
                else:
                    AionShellError("couldn't find 'skill.aion' or 'plugin.aion' in " + dir + ". See 'create_skill_file' function in 'aionlib.skill' to create a 'skill.aion' file"
                                   "or 'create_plugin_file' function in 'aionlib.plugin' to create a 'plugin.aion' file", no_skill_plugin_file_errno)
            else:
                AionShellError("couldn't find directory " + dir, no_dir_errno)

        elif command == "pid":
            arglen_check(args.command, 1)
            is_aion_running(command)
            import variable
            avar = variable.Variable()
            print(avar.get_value("AION_PID"))

        elif command == "save":
            arglen_check(args.command, 2)
            import save as asave
            asave.save(args.command[1])

        elif command == "saves":
            arglen_check(args.command, 1)
            import save as asave
            print(" ".join(asave.saves()))

        elif command in ["remove", "uninstall"]:  # UnRem
            errno = "07340"
            arglen_check(args.command, 2)
            package = args.command[1]
            if command == "uninstall":
                name = "Uninstall"
            else:
                name = "Remove"
            question = yesno(name + " " + package + "? (y/n): ")
            if name == "Remove":
                name = "Remov"
            if package == "aion":
                if question is True:
                    question = yesno("Should your personal data ('/etc/aion_data/': custom skills / plugins, version saves, language files, ...) deleted as well? (y/n): ")
                    UnRem.aion(question)
                    print(name + "ed aion")
                    print("You should reboot now to complete the " + name.lower() + " process")
            elif package == "aionlib":
                if question is True:
                    UnRem.aionlib()
                    print(name + "ed aionlib")
            elif package == "respeaker":
                if question is True:
                    UnRem.respeaker()
                    print(name + "ed respeaker")
            else:
                package_type = which_package(package, "Type in the number of your package type: ")
                if package_type == -1:
                    AionShellError("couldn't find skill / plugin " + package, errno)
                elif package_type == 0:
                    UnRem.skill(package)
                elif package_type == 1:
                    UnRem.run_after_plugin(package)
                elif package_type == 2:
                    UnRem.run_before_plugin(package)

        elif command in ["run", "start"]:
            arglen_check(args.command, 1)
            import start
            from os import geteuid
            if geteuid() == 0:
                start(True)
            elif geteuid() == 1000:
                start(False)

        elif command == "update":
            errno = "43503"
            arglen_check(args.command, 2)
            package = args.command[1]
            if package == "aion":
                Update.aion()
            elif package == "aionlib":
                Update.aionlib()
            else:
                package_type = which_package(package, "Type in the number of your package type: ")
                if package_type == -1:
                    AionShellError("couldn't find skill / plugin " + package, errno)
                elif package_type == 0:
                    Update.skill(package)
                elif package_type == 1:
                    Update.run_after_plugin(package)
                elif package_type == 2:
                    Update.run_before_plugin(package)

        elif command == "variable":
            arglen_check(args.command, 2)
            command_variable = args.command[1]
            import variable
            avar = variable.Variable()
            print(avar.get_value(command_variable))

        elif command == "version":
            errno = "56297"
            arglen_check(args.command, 2)
            package = args.command[1]
            if package == "aion":
                Version.aion()
            elif package == "aionlib":
                Version.aionlib()
            else:
                package_type = which_package(package, "Type in the number of your package type: ")
                if package_type == -1:
                    AionShellError("couldn't find skill / plugin " + package, errno)
                elif package_type == 0:
                    Version.skill(package)
                elif package_type == 1:
                    Version.run_after_plugin(package)
                elif package_type == 2:
                    Version.run_before_plugin(package)

        else:
            errno = "12345"
            AionShellError(" ".join(args.command) + " isn't a command. Type 'aion help' to get help", errno)

    except KeyboardInterrupt:
        exit(-1)
