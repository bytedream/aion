#!/usr/bin/python3

try:
    from .utils import aion_data_path as _aion_data_path
except ImportError:
    from utils import aion_data_path as _aion_data_path


save_path = _aion_data_path + "/saves"


def load_save(name: str, current_save_name: str = None) -> None:
    """
    loads a saved aion_data

    :param name: str
        name of  the  new aion_data save
        syntax: "<name>"
        example: "test save"
    :param current_save_name: str, optional
        if not None, the current aion_data get saved under this name
        syntax: "<current save name>"
        example: "test save2"
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import save_save_not_found
    except ImportError:
        from _error_codes import save_save_not_found

    from os import listdir
    from shutil import copytree, rmtree

    if name not in listdir(save_path):
        raise NotADirectoryError("Errno: " + save_save_not_found + " - Couldn't find the save '" + name + "'")
    else:
        if current_save_name:
            save(current_save_name)
        rmtree(_aion_data_path)
        copytree(save_path + "/" + name, _aion_data_path)


def save(name: str) -> None:
    """
    saves the current aion_data directory

    :param name: str
        name of the save
        syntax: "<name>"
        example: "test save"
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import save_save_name_already_exist
        from .utils import BaseXMLWriter
    except ImportError:
        from _error_codes import save_save_name_already_exist
        from utils import BaseXMLWriter

    from os import listdir
    from shutil import copytree

    if name in listdir(save_path):
        raise NameError("Errno: " + save_save_name_already_exist + " - The save name '" + name + "' already exists")
    else:
        copytree(_aion_data_path, save_path + "/" + name)


def saves() -> list:
    """
    get all aion_data saves

    :return: list
        returns a list of the names of the aion_data saves
        syntax: [<saves>]
        example: ["test save", "test save2"]

    :since: 0.1.0
    """
    from os import listdir

    return_list = []

    for file in listdir(save_path):
        return_list.append(file)

    return return_list
