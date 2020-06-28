#!/usr/bin/python3

import xml.etree.ElementTree as _ET
from glob import glob as _glob
from xml.dom import minidom as _minidom

aion_data_path = "/etc/aion_data"
aion_path = "".join(_glob("/usr/local/aion-*"))


def get_location_infos_by_ip(ip_address: str = None) -> dict:
    """
    get infos about the user via ip address

    :param ip_address: str, optional
        ip address from which you want to get the infos (leave None if you want to use the local ip address)
        syntax: <ip address>
        example: "216.58.206.14"
    :return: dict
        returns dict with informations
        syntax: {"ip": <ip address>,
                "hostname": <hostname>,
                "city": <city>,
                "region": <region>,
                "country": <county>,
                "loc": <gps location>,
                "org": <internet provider>,
                "postal": <postal>,
                "timezone": <timezone>,
                "readme": 'https://ipinfo.io/missingauth'}
        example: {"ip": "0.0.0.0",
                "hostname": "examplehostname",
                "city": "examplecity",
                "region": "exampleregion",
                "country": "US,
                "loc": "examplegps",
                "org": "exampleprovider",
                "postal": "examplepostal",
                "timezone": "exampletimezone",
                "readme": 'https://ipinfo.io/missingauth'}

    :since: 0.1.0
    """
    from urllib.request import urlopen
    from json import load

    if ip_address is None:
        return load(urlopen("https://ipinfo.io/json"))
    else:
        return load(urlopen("https://ipinfo.io/" + ip_address + "/json"))


def get_full_directory_data(directory: str) -> list:
    """
    returns list of all files and directories of given directory back (subdirectories with subfiles, subsubdirectories with subsubfiles, ... included)

    :param directory: str
        path of directory from which you want to get the data
        syntax: <directory path>
        example: "/home/pi"
    :return: list
        list of all files and directories (subdirectories with subfiles, subsubdirectories with subsubfiles, ... included)
        syntax: [<path>]
        example: ["/home/pi/test", "/home/pi/test/test.py"]

    :since: 0.1.0
    """
    from os import walk
    from os.path import join

    data = []
    for path, subdirs, files in walk(directory):
        for name in files:
            data.append(join(path, name))
    return data


def get_full_youtube_audio_url(search_element: str) -> str:
    """
    search youtube for the search element and gives the first youtube url back

    :param search_element: str
        the element you want to search
        syntax: <search element>
        example: "Every programming tutorial"
    :return: str
        the youtube url from the search element
        syntax: <url>
        example: "https://youtu.be/MAlSjtxy5ak"

    :since: 0.1.0
    """
    import urllib.parse, urllib.request
    from pafy import new
    from re import findall
    search_query = urllib.parse.urlencode({"search_query": search_element})
    for i in range(10):  # sometimes the video url's cannot be found
        try:
            html_content = urllib.request.urlopen("https://www.youtube.com/results?" + search_query)
            search_results = findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            return new(str("https://www.youtube.com/watch?v=" + search_results[0])).getbestaudio().url
        except IndexError:
            pass


def is_dict_in_dict(dict1: dict, dict2: dict) -> bool:
    """
    checks if dict key-value pairs exist in another dict

    :param dict1: dict
        dictionary you want to check if it is included in another dictionary
        syntax: {"key": "value"}
        example: {"a": "b"}
    :param dict2: dict
        dictionary you want to see if there is another dictionary in it
        syntax: {"key": "value"}
        example: {"a": "b", "c": "d"}
    :return: boolean
        returns if 'dict1' is in 'dict2'
        syntax: <boolean>
        example: True

    :since: 0.1.0
    """
    for key, value in dict1.items():
        if key in dict2:
            if dict2[key] == value:
                pass
            else:
                return False
        else:
            return False

    return True


def is_element_in_file(fname: str, element: str) -> bool:
    """
    checks if an element is in a file

    :param fname: str
        file name of file
        syntax: <file name>
        example: "/home/pi/test.py"
    :param element: str
        element you want to check if in file
        syntax: <element>
        example: "test"
    :return: bool
        returns True or False is element is in file
        syntax: <boolean>
        example: True

    :since: 0.1.0
    """
    is_in_file = False
    for line in open(fname, "r"):
        if element in line:
            is_in_file = True
            break
    return is_in_file


def is_internet_connected() -> bool:
    """
    checks if the internet is connected

    :return: bool
        returns True or False if internet is connected
        syntax: <boolean>
        example: True

    :since: 0.1.0
    """
    try:
        from ._error_codes import utils_unexpected_error
    except ImportError:
        from _error_codes import utils_unexpected_error

    import socket
    try:
        socket.gethostbyname("google.com")
        internet = True
    except OSError:
        internet = False
    except:
        raise OSError("Errno: " + utils_unexpected_error + " - An unexpected error occurred")
    return internet


def is_root() -> bool:
    """
    checks if the function from which this function is called run as root

    :return: bool
        returns True or False if the function from which this function is called run as root
        syntax: <boolean>
        example: True

    :since: 0.1.0
    """
    from os import geteuid
    if geteuid() == 0:
        return True
    elif geteuid() == 1000:
        return False


def remove_brackets(string: str) -> str:
    """
    removes all brackets and the text which is between the brackets

    :param string: str
        string from which you want to remove the brackets
        syntax: "<string>"
        example: "Hello, this is(wedcwerfwe) an [sdvsfvv] random text{ervweg}"
    :return: str
        string without brackets and the text between them
        syntax: "<string without brackets>"
        example: "Hello, this is an random text"

    :since: 0.1.0
    """
    finished_string = ""
    square_brackets = 0
    parentheses = 0
    for brackets in string:
        if brackets == "[":
            square_brackets += 1
        elif brackets == "(":
            parentheses += 1
        elif brackets == "]" and square_brackets > 0:
            square_brackets -= 1
        elif brackets == ")" and parentheses > 0:
            parentheses -= 1
        elif square_brackets == 0 and parentheses == 0:
            finished_string += brackets
    return finished_string


def remove_space(string: str, space: str = "  ") -> str:
    """
    removes all the space from string which is equal or higher than from argument 'space' given space

    :param string: str
        string from which you want to remove space
        syntax: "<string>"
        example: "This string has     to   much space"
    :param space: str, optional
        space size from which you want to start to remove
        syntax: "<space>"
        example: "  "
        NOTE: '"  "' will be replaced with '" "'
    :return: str
        returns the string without the given space and higher
        syntax: "<string>"
        example: "This string has to much space"

    :since: 0.1.0
    """
    while True:
        if space in string:
            string = string.replace(space, "")
        space = space + " "
        if len(space) >= len(string):
            break

    string = string.strip()
    return string


def remove_string_characters(string: str, characters_to_remove: (list, tuple)) -> str:
    """
    removes in argument 'characters_to_remove' given characters from given string

    :param string: str
        string from which you want to remove the characters
        syntax: "<string>"
        example: "This string hello has its to much word me"
    :param characters_to_remove: (list, tuple)
        list of characters you want to remove from string
        syntax: [<character>]
        example: ["hello", "its", "me"]
    :return: str
        returns string without in given characters to remove
        syntax: "<string>"
        example: "This string has to much word"

    :since: 0.1.0
    """
    for char in characters_to_remove:
        if char in string:
            string = string.replace(char, "")
    return string


def remove_string_sequence(string: str, start: str, end: str, include: bool = False) -> str:
    """
    removes all characters from a string between the given 'start' and 'end' element

    :param string: str
        the string from which the sequence should be removed from
        syntax: "<string>"
        example: "Test lol random words string"
    :param start: str
        start character
        syntax: "<start character>"
        example: "lol"
    :param end: str
        end character
        syntax: "<end character>"
        example: "words"
    :param include: bool
        'True' if the given start and end character should be included in the return string, False if not
        syntax: <boolean>
        example: False
    :return: str
        string without the sequence between 'start' and 'end'
        syntax: "<string>"
        example: "Test  string"

    :since: 0.1.0
    """
    if include:
        return string.replace(string[string.find(start) - len(start):string.find(end)], "")
    return string.replace(string[string.find(start):string.find(end) + len(end)], "")


def replace_line(fname: str, line_number: int, new_line: str) -> None:
    """
    replaces a line in a file

    :param fname: str
        filename from which you want to replace the line
        syntax: <filename>
        example: "/home/pi/test.txt"
    :param line_number: int
        line number of line you want to replace
        syntax: <line number>
        example: "5"
    :param new_line: str
        line content with which the line should be replaced
        syntax: <new line>
        example: "This is the new line"
    :return: None

    :since: 0.1.0
    """
    try:
        from ._error_codes import utils_fname_doesnt_exist
    except ImportError:
        from _error_codes import utils_fname_doesnt_exist
    from os.path import isfile

    line_number = int(line_number)
    if isfile(fname) is False:
        raise FileNotFoundError("Errno: " + utils_fname_doesnt_exist + " - " + fname + " doesn't exist")
    lines = open(fname).readlines()
    lines[line_number] = new_line + "\n"
    with open(fname, "w") as file:
        file.writelines(lines)
        file.close()


def vlc(url_or_file_path: str, video: bool = False) -> None:
    """
    plays audio from url or file path

    :param url_or_file_path: str
        the url or the path of the file you want to play
        syntax: <url or path>
        example: "https://youtu.be/MAlSjtxy5ak"
    :param video: bool, optional
        sets True or False if video should be played (if the file had one)
        syntax: <boolean>
        example: False
    :return: None

    :since: 0.1.0
    """
    from os import system

    if isinstance(video, bool) is False:
        raise TypeError("expected " + str(bool.__name__) + " for video, got " + str(type(video).__name__))
    if video is True:
        system('cvlc --play-and-exit "' + url_or_file_path + '"')
    else:
        system('cvlc --play-and-exit --no-video "' + url_or_file_path + '"')


class BaseXMLBuilder:
    """
    a class to simple build an '.xml' file

    :since: 0.1.0
    """

    def __init__(self, root_name: str = "root", **root_extra: str) -> None:
        """
        :param root_name: str, optional
            name of the root element of the xml file
            syntax: "<root name>"
            example: "root"
        :param root_extra: kwargs, optional
            attributes for the root element
            syntax: <key>="<value>"
            example: author="blueShard"
        :return: None

        :since: 0.1.0
        """
        self.root_name = root_name

        self._element_list = [self.root_name]
        self._root = _ET.Element(root_name, **root_extra)

    def _prettify(self, string: str = None) -> str:
        """
        prettifies the given string

        :param string: str
            string to prettify
            syntax: <string>
            example: "<root><test_element></test_element></root>"
        :return: str
            returns the_prettified string
            syntax: <string>
            example: "<root>
                        <test_element>
                        </test_element>
                      </root>"

        :since: 0.1.0
        """
        if string is None:
            reparsed = _minidom.parseString(_ET.tostring(self._root, "utf-8"))
        else:
            reparsed = _minidom.parseString(bytes(string, "utf-8", errors="ignore"))
        pre_output = reparsed.toprettyxml(indent="  ")
        return "\n".join(pre_output.split("\n")[1:])

    def create_root_element(self, name: str, text: str = None, attrib: dict = {}, **extra: str) -> None:
        """
        creates a new entry as a sub element of the root element

        :param name: str
            name of the new element
            syntax: "<name>"
            example: "root_child"
        :param text: str, optional
            text of the new element
            syntax: "<text>"
            example: "This is a root element"
        :param attrib: dict, optional
            attributes for the new element
            syntax: {"<key>", "<value>"}
            example: {"author": "blueShard"}
        :param extra: kwargs, optional
            attributes for the new element
            syntax: <key>="<value>"
            example: author="blueShard"
        :return: None

        :since: 0.1.0
        """
        if text:
            element = _ET.Element(name, attrib, **extra).text = text
        else:
            element = _ET.Element(name, attrib, **extra)

        self._root.append(element)
        self._element_list.append(name)

    def create_sub_element(self, parent_name: str, name: str, text: str = None, attrib: dict = {}, parent_attrib: dict = None, **extra: str) -> None:
        """
        creates a sub element of an parent element

        :param parent_name: str
            name of the parent element to which the sub element should be added
            syntax: <parent name>
            example: "root_child"
        :param name: str
            name of the new sub element you want to add
            syntax: <name>
            example: "sub_child"
        :param text: str, optional
            text of the new sub element
            syntax: <text>
            example: "This is a sub element"
        :param attrib: dict, optional
            attributes for the new element
            syntax: {<key>, <value>}
            example: {"author": "blueShard"}
        :param parent_attrib: dict, optional
            attributes of the new sub element
            syntax: {<key>: <value>}
            example: {"language": "en_US"}
        :param extra: kwargs, optional
            attributes of the new sub element
            syntax: <key>=<value>
            example: language="en_US"
        :return: None

        :since: 0.1.0
        """
        try:
            from ._error_codes import utils_couldnt_find_parent
        except ImportError:
            from _error_codes import utils_couldnt_find_parent

        if parent_name in self._element_list:
            for parent in self._root.iter(parent_name):
                if parent_attrib:
                    if parent.attrib == parent_attrib:
                        if text:
                            _ET.SubElement(parent, name, attrib, **extra).text = text
                        else:
                            _ET.SubElement(parent, name, attrib, **extra)
                        self._element_list.append(name)
                else:
                    if text:
                        _ET.SubElement(parent, name, attrib, **extra).text = text
                    else:
                        _ET.SubElement(parent, name, attrib, **extra)
                    self._element_list.append(name)
        else:
            raise IndexError("Errno: " + utils_couldnt_find_parent + " - Couldn't find parent '" + parent_name + "'. The available parents are in this list: " + str(self._element_list))

    def get_string(self, pretty_print: bool = True) -> str:
        """
        get sting of the xml tree

        :param pretty_print: bool, optional
            sets True or False if the xml tree string should be pretty printed
            syntax: <boolean>
            example: True
        :return: str
            returns the string of the builded xml tree
            syntax: <xml tree>
            example: <root>
                       <root_child author="blueShard">
                         <sub_child>This is a sub element</sub_child>
                       </root_child>
                     </root>

        :since: 0.1.0
        """
        if pretty_print is True:
            return self._prettify()
        else:
            return _ET.tostring(self._root, "utf-8").decode("ascii")

    def write(self, fname: str, mode: str = "w", pretty_print: bool = True) -> None:
        """
        writes the xml tree to a file

        :param fname: str
            filename of file you want to write
            syntax: <filename>
            example: "/home/pi/text.xml"
        :param mode: str, optional
            mode to write on file
            syntax: <mode>
            example: "w"
        :param pretty_print: bool, optional
            sets True or False if the xml tree string should be pretty printed
            syntax: <boolean>
            example: True
        :return: None

        :since: 0.1.0
        """
        with open(fname, mode=mode) as file:
            file.write(self.get_string(pretty_print))
            file.close()


class BaseXMLReader:

    """
    a class to simple read a '.xml' file

    :since: 0.1.0
    """

    def __init__(self, fname: str) -> None:
        """
        makes the fname available for all class methods and set all variables

        :param fname: str
            filename of the file you want to read
            syntax: <filename>
            example: "/home/pi/test.xml"
        :return: None

        :since: 0.1.0
        """
        self.fname = fname

        self._tree = _ET.parse(self.fname)
        self._root = self._tree.getroot()

        self.get_infos._root = self._root

    def _prettify(self, string: str = None) -> str:
        """
        prettifies the given string

        :param string: str
            string to prettify
            syntax: <string>
            example: "<root><test_element></test_element></root>"
        :return: str
            returns the_prettified string
            syntax: <string>
            example: "<root>
                        <test_element>
                        </test_element>
                      </root>"

        :since: 0.1.0
        """
        if string is None:
            reparsed = _minidom.parseString(_ET.tostring(self._root, "utf-8"))
        else:
            reparsed = _minidom.parseString(bytes(string, "utf-8", errors="ignore"))
        pre_output = reparsed.toprettyxml(indent="  ")
        return "\n".join(pre_output.split("\n")[1:])

    class get_infos(dict):
        """
        a modified dict class with indexing items

        :since: 0.1.0
        """

        def __init__(self, elem_tags: (str, list) = []) -> dict:
            """
            get infos about an element in the file

            :param elem_tags: (str, list)
                name of elements you want to get infos about
                syntax: [<element tags>]
                example: ["sub_child"]
            :return: dict
                returns a dict of names from the given elements with a list of dictionaries of found elements (complex description xD)
                syntax: {<element>: [{"parent": {"tag": <parent tag>, "text": <text of the parent element>, "attrib": {<attributes of the parent element>}}, "childs": [<childs of the element>], "tag": <tag of the element>, "text": <text of the element>, "attrib": {<attributes of the element>}}]}
                example: {"sub_child": [{"parent": {"tag": "root_child", "text": "", "attrib": {"author": "blueShard"}}, "childs": ["sub_child"], "tag": "sub_child", "text": "This is a sub element", "attrib": {}}]}

            :since: 0.1.0
            """
            if isinstance(elem_tags, str):
                elem_tags = [elem_tags]

            child_list = []
            return_dict = {}
            for elem in elem_tags:
                if elem == "<all>":
                    continue
                elif elem == "<root>":
                    return_dict[self._root.tag] = []
                else:
                    return_dict[elem] = []

            all_child_list = []

            if "<all>" in elem_tags:
                if self._root.tag in return_dict:
                    pass
                else:
                    return_dict[self._root.tag] = []
                return_dict[self._root.tag].append(
                    {"parent": {"tag": "", "text": "", "attrib": {}}, "childs": [child.tag for child in self._root], "tag": self._root.tag, "text": "", "attrib": self._root.attrib})
                for root_child in self._root:
                    if root_child.tag in return_dict:
                        pass
                    else:
                        return_dict[root_child.tag] = []
                    return_dict[root_child.tag].append(
                        {"parent": {"tag": self._root.tag, "text": self._root.text, "attrib": self._root.attrib}, "childs": [sub_root_child.tag for sub_root_child in root_child],
                         "tag": root_child.tag, "text": root_child.text, "attrib": root_child.attrib})
                    all_child_list.append(root_child)
                for parent in list(all_child_list):
                    for child in parent:
                        if child.tag in return_dict:
                            pass
                        else:
                            return_dict[child.tag] = []
                        return_dict[child.tag].append(
                            {"parent": {"tag": parent.tag, "text": parent.text, "attrib": parent.attrib}, "childs": [sub_child.tag for sub_child in child], "tag": child.tag, "text": child.text,
                             "attrib": child.attrib})
                        all_child_list.append(child)
                        if child in all_child_list:
                            all_child_list.remove(child)
            else:
                if self._root.tag in return_dict:
                    return_dict[self._root.tag].append({"parent": {}, "childs": [child.tag for child in self._root], "tag": self._root.tag, "text": "", "attrib": self._root.attrib})
                for root_child in self._root:
                    if root_child.tag in return_dict:
                        return_dict[root_child.tag].append(
                            {"parent": {"tag": self._root.tag, "text": self._root.text, "attrib": self._root.attrib}, "childs": [sub_root_child.tag for sub_root_child in root_child],
                             "tag": root_child.tag, "text": root_child.text, "attrib": root_child.attrib})
                    else:
                        child_list.append(root_child)
                for parent in list(child_list):
                    for child in parent:
                        if child.tag in return_dict:
                            return_dict[child.tag].append(
                                {"parent": {"tag": parent.tag, "text": parent.text, "attrib": parent.attrib}, "childs": [sub_child.tag for sub_child in child], "tag": child.tag, "text": child.text,
                                 "attrib": child.attrib})
                        else:
                            child_list.append(child)
                        if child in child_list:
                            child_list.remove(child)

            self._return_dict = return_dict

            self.items._return_dict_keys = return_dict.keys()
            self.items._return_dict_values = return_dict.values()
            self.keys._return_dict_keys = return_dict.keys()
            self.values._return_dict_values = return_dict.values()

            super().__init__(self._return_dict)

        def __iter__(self):
            return iter(self._return_dict)

        def __next__(self):
            return self._return_dict

        def __repr__(self):
            return self._return_dict

        def __str__(self):
            return str(self._return_dict)

        def index(self, index: int) -> dict:
            """
            index a key-value pair in a dict

            :param index: int
                index of the key-value pair you want to get
                syntax: <index>
                example: 5
            :return: dict
                returns the key-value pair of the given index
                syntax: {<key>: <value>}
                example: {"test_key": "test_value"}

            :since: 0.1.0
            """
            try:
                from ._error_codes import utils_dict_index_out_of_range
            except ImportError:
                from _error_codes import utils_dict_index_out_of_range

            i = 0
            for key, value in self._return_dict.items():
                if i == index:
                    return {key: value}
                else:
                    i += 1
            raise IndexError("Errno: " + utils_dict_index_out_of_range + " - Dict index out of range")

        class items:
            """
            a modified items() function from dict with indexing items
            """

            def __init__(self):
                pass

            def __getitem__(self, item):
                return tuple(self._return_dict_items)[item]

            def __iter__(self):
                return iter(self._return_dict_items)

            def __len__(self):
                return len(self._return_dict_items)

            def __next__(self):
                return self._return_dict_items

            def __repr__(self):
                return self._return_dict_items

            def __str__(self):
                return str(self._return_dict_items)

            def index(self, index: int):
                """
                index a key-value pair in a dict

                :param index: int
                    index of the key-value pair you want to get
                    syntax: <index>
                    example: 5
                :return: the given index in the values

                :since: 0.1.0
                """
                return {list(self._return_dict_keys)[index]: list(self._return_dict_values)[index]}

        class keys:
            """
            a modified keys() function from dict with indexing items
            """

            def __init__(self):
                pass

            def __iter__(self):
                return iter(self._return_dict_keys)

            def __len__(self):
                return len(list(self._return_dict_keys))

            def __next__(self):
                return self._return_dict_keys

            def __repr__(self):
                return self._return_dict_keys

            def __str__(self):
                return str(self._return_dict_keys)

            def index(self, index: int):
                """
                index a key in a dict

                :param index: int
                    index of the key you want to get
                    syntax: <index>
                    example: 5
                :return: the given index in the keys

                :since: 0.1.0
                """
                return list(self._return_dict_keys)[index]

        class values:
            """
            a modified values() function from dict with indexing items
            """

            def __init__(self):
                pass

            def __iter__(self):
                return iter(self._return_dict_values)

            def __len__(self):
                return len(list(self._return_dict_values))

            def __next__(self):
                return self._return_dict_values

            def __repr__(self):
                return self._return_dict_values

            def __str__(self):
                return str(self._return_dict_values)

            def index(self, index: int):
                """
                index a value in a dict

                :param index: int
                    index of the value you want to get
                    syntax: <index>
                    example: 5
                :return: the given index in the values

                :since: 0.1.0
                """
                return list(self._return_dict_values)[index]

    def get_string(self, pretty_print: bool = True) -> str:
        """
        gets the string of the xml tree in the file

        :param pretty_print: bool, optional
            sets True or False if the xml tree string should be pretty printed
            syntax: <boolean>
            example: True
        :return: str
            returns the string of the xml tree
            syntax: <xml tree>
            example: "<root>
                        <root_child author="blueShard">
                          <sub_child>This is a sub element</sub_child>
                        </root_child>
                      </root>"

        :since: 0.1.0
        """
        string = _ET.tostring(self._root, "utf-8").decode("ascii")
        if pretty_print is True:
            if "\n" in string:
                return string
            else:
                return self._prettify()
        else:
            if "\n" in string:
                return "".join([line.strip() for line in _ET.tostring(self._root, "utf-8").decode("ascii").split("\n")])
            else:
                return string


class BaseXMLWriter:
    """
    a class to simple change/write a '.xml' file

    :since: 0.1.0
    """

    def __init__(self, fname: str, auto_write: bool = False) -> None:
        """
        makes the fname and auto_write available for all class methods and set all variables

        :param fname : str
            filename of the file you want to write to
            syntax: <filename>
            example: "/home/pi/test.xml"
        :param auto_write : bool, optional
            sets if after every change to the getted xml tree the changes should be write to the file
            syntax: <boolean>
            example: False
        :return: None

        :since: 0.1.0
        """
        self.auto_write = auto_write
        self.fname = fname

        self._root = _ET.fromstring("".join([item.replace("\n", "").strip() for item in [line for line in open(self.fname, "r")]]))

    def _prettify(self, string: str = None) -> str:
        """
        prettifies the given string

        :param string: str
            string to prettify
            syntax: <string>
            example: "<root><test_element></test_element></root>"
        :return: str
            returns the_prettified string
            syntax: <string>
            example: "<root>
                        <test_element>
                        </test_element>
                      </root>"

        :since: 0.1.0
        """
        if string is None:
            reparsed = _minidom.parseString(_ET.tostring(self._root, "utf-8"))
        else:
            reparsed = _minidom.parseString(string)
        pre_output = reparsed.toprettyxml(indent="  ")
        return "\n".join(pre_output.split("\n")[1:])

    def add(self, parent_tag: str, elem_tag: str, text: str = None, attrib: dict = {}, parent_attrib: dict = None, **extra: str) -> None:
        """
        adds an element to xml tree

        :param parent_tag : str
            name of the parent element
            syntax: <parent name>
            example: "root_child"
        :param elem_tag : str
            name of the element you want to add
            syntax: <element name>
            example: "second_sub_child"
        :param text : str, optional
            text of the element you want to add
            syntax: <text>
            example: "This is the second sub child"
        :param attrib : dict
            attributes for the new element
            syntax: {<key>, <value>}
            example: {"author": "blueShard"}
        :param parent_attrib : dict, optional
            attributes of the parent element
            syntax: {<key>: <value>}
            example: {"author": "blueShard"}
        :param extra : kwargs, optional
            attributes of the new element
            syntax: <key>=<value>
            example: language="de_DE"
        :return: None

        :since: 0.1.0
        """
        if parent_tag == "<root>":
            parent_tag = self._root.tag

        if parent_tag == self._root.tag:
            if parent_attrib:
                if parent_attrib == self._root.attrib:
                    if text:
                        root_text_element = _ET.Element(elem_tag, attrib, **extra)
                        root_text_element.text = text
                        self._root.append(root_text_element)
                    else:
                        self._root.append(_ET.Element(elem_tag, attrib, **extra))
            else:
                if text:
                    root_text_element = _ET.Element(elem_tag, attrib, **extra)
                    root_text_element.text = text
                    self._root.append(root_text_element)
                else:
                    self._root.append(_ET.Element(elem_tag, attrib, **extra))
        else:
            for parent in self._root.iter(parent_tag):
                if parent_attrib:
                    if parent.attrib == parent_attrib:
                        if text:
                            _ET.SubElement(parent, elem_tag).text = text
                        else:
                            _ET.SubElement(parent, elem_tag, attrib, **extra)
                else:
                    if text:
                        _ET.SubElement(parent, elem_tag).text = text
                    else:
                        _ET.SubElement(parent, elem_tag, attrib, **extra)

        if self.auto_write is True:
            self.write()

    def get_string(self, pretty_print: bool = False) -> str:
        """
        gets the string of the xml tree in the file

        :param pretty_print: bool, optional
            sets True or False if the xml tree string should be pretty printed
            syntax: <boolean>
            example: True
        :return: str
            returns the string of the xml tree
            syntax: <xml tree>
            example: "<root>
                        <root_child author="blueShard">
                          <sub_child>This is a sub element</sub_child>
                          <second_sub_child language="de_DE"/>
                        </root_child>
                      </root>"

        :since: 0.1.0
        """
        string = _ET.tostring(self._root, "utf-8").decode("ascii")
        if pretty_print is True:
            if "\n" in string:
                return string
            else:
                return self._prettify()
        else:
            if "\n" in string:
                return "".join([line.strip() for line in _ET.tostring(self._root, "utf-8").decode("ascii").split("\n")])
            else:
                return string

    def remove(self, parent_tag: str, elem_tag: str, parent_attrib: dict = None) -> None:
        """
        removes an element from the xml tree

        :param parent_tag : str
            name of the parent element
            syntax: <parent name>
            example: "root_child"
        :param elem_tag : str
            name of the element you want to remove
            syntax: <element name>
            example: "second_sub_child"
        :param parent_attrib : dict, optional
            attributes of the parent element
            syntax: {<key>: <value>}
            example: {"author": "blueShard"}
        :return: None

        :since: 0.1.0
        """
        if parent_tag == "<root>":
            parent_tag = self._root.tag

        if parent_tag == self._root.tag:
            for child in self._root:
                if child.tag == elem_tag:
                    if parent_attrib:
                        if self._root.attrib == parent_attrib:
                            self._root.remove(child)
                    else:
                        self._root.remove(child)

        for parent in self._root.iter(parent_tag):
            for child in parent:
                if child.tag == elem_tag:
                    if parent_attrib:
                        if parent.attrib == parent_attrib:
                            parent.remove(child)
                    else:
                        parent.remove(child)

        if self.auto_write is True:
            self.write()

    def update(self, parent_tag: str, elem_tag: str, text: str = None, attrib: dict = {}, parent_attrib: dict = None, **extra: str) -> None:
        """
        updates an element in the xml tree

        :param parent_tag : str
            name of the parent element
            syntax: <parent name>
            example: "root_child"
        :param elem_tag : str
            name of the element you want to update
            syntax: <element name>
            example: "second_sub_child"
        :param text : str, optional
            new text of the updated element
            syntax: <text>
            example: "New text of the second sub child"
        :param attrib : dict
            attributes for the new element
            syntax: {<key>, <value>}
            example: {"author": "blueShard"}
        :param parent_attrib : dict, optional
            attributes of the parent element
            syntax: {<key>: <value>}
            example: {"author": "blueShard"}
        :param extra : kwargs, optional
           new attributes of the updated element
            syntax: <key>=<value>
            example: language="de_DE"
        :return: None

        :since: 0.1.0
        """
        if parent_tag == "<root>":
            parent_tag = self._root.tag

        if parent_tag == self._root.tag:
            for child in self._root:
                if child.tag == elem_tag:
                    if parent_attrib:
                        if self._root.attrib == parent_attrib:
                            if text:
                                child.text = str(text)
                            for key, value in attrib.items():
                                child.set(str(key), str(value))
                            for key, value in extra.items():
                                child.set(key, str(value))
                    else:
                        if text:
                            child.text = str(text)
                        for key, value in attrib.items():
                            child.set(str(key), str(value))
                        for key, value in extra.items():
                            child.set(key, str(value))
        for parent in self._root.iter(parent_tag):
            for child in parent:
                if child.tag == elem_tag:
                    if parent_attrib:
                        if parent.attrib == parent_attrib:
                            if text:
                                child.text = str(text)
                            for key, value in attrib.items():
                                child.set(str(key), str(value))
                            for key, value in extra.items():
                                child.set(key, str(value))
                    else:
                        if text:
                            child.text = str(text)
                        for key, value in attrib.items():
                            child.set(str(key), str(value))
                        for key, value in extra.items():
                            child.set(key, str(value))

        if self.auto_write is True:
            self.write()

    def write(self, mode: str = "w", pretty_print: bool = True) -> None:
        """
        writes the xml tree to a file

        :param mode : str, optional
            mode to write on file
            syntax: <mode>
            example: "w"
        :param pretty_print : bool, optional
            sets True or False if the xml tree string should be pretty printed
            syntax: <boolean>
            example: True
        :return: None

        :since: 0.1.0
        """
        with open(self.fname, mode=mode) as file:
            if pretty_print is False:
                file.write(_ET.tostring(self._root, "utf-8").decode("ascii"))
            else:
                file.write(self._prettify())
            file.close()
