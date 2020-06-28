#!/usr/bin/env python3

def acc_file_search(file_name, search_element):
    import re
    not_needed_informations = ["author=", "version=", "command_type="]
    no_square_bracket = ["name=", "author=", "version=", "command_type="]
    if "=" not in search_element:
        search_element = search_element + "="
    fileprint = open(file_name).read().splitlines()
    acc_search_line = acc_search_file_element(file_name, search_element)
    acc_file_search = fileprint[acc_search_line]
    acc_file_line = []
    if search_element in acc_file_search:
        acc_file_search = acc_file_search.replace(search_element, "")
        if "\n" in acc_file_search:
            acc_file_search = acc_file_search.replace("\n", "")
        acc_file_line.append(acc_file_search)
        if "]" not in acc_file_search:
            if search_element in no_square_bracket:
                pass
            elif search_element not in no_square_bracket:
                acc_first_square_bracket_line = acc_search_file_element(file_name, search_element)
                acc_second_square_bracket_line = acc_search_file_element(file_name, "]", acc_first_square_bracket_line)
                while True:
                    bracket_lines = list(range(acc_first_square_bracket_line, acc_second_square_bracket_line + 1))
                    elements = []
                    for element_numbers in bracket_lines:
                        element_list = fileprint[element_numbers]
                        if search_element in element_list:
                            if not "=" in search_element:
                                search_element = search_element + "="
                            element_list = element_list.replace(search_element, "")
                        element_list = element_list.lstrip()
                        elements.append(element_list)

                    acc_file_line = elements
                    break

    global acc_file
    acc_file_temporary = []
    for acc_file in acc_file_line:
        acc_file = acc_file
        if acc_file == "":
            if search_element in not_needed_informations:
                if "=" in search_element:
                    search_element = search_element.replace("=", "")
                acc_file = ("There is no " + search_element)
                return acc_file
            elif search_element not in not_needed_informations:
                if "=" in search_element:
                    search_element = search_element.replace("=", "")
                    pass
                acc_file = ("There is no " + search_element + ", but it must be something indicated!")
                return acc_file
            else:
                acc_file = "An error appears!"
                return acc_file
        if "[" in acc_file:
            acc_file = acc_file.replace("[", "")
        if "]" in acc_file:
            acc_file = acc_file.replace("]", "")
        if '"' in acc_file:
            acc_file = acc_file.replace('"', "")
        acc_file_temporary.append(acc_file)
        if len(acc_file_temporary) > 1:
            acc_file = (", ".join(acc_file_temporary))
        else:
            acc_file = ("".join(acc_file_temporary))
        if ",," in acc_file:
            acc_file = acc_file.replace(",,", ",")
        if re.search("[a-zA-Z]", acc_file) == None:
            if search_element in no_square_bracket:
                if "=" in search_element:
                    search_element = search_element.replace("=", "")
            print("There is no " + search_element + ", but it must be something indicated!")

    return acc_file

def acc_search_file_element(file_name, search_element, from_line=0):
    if "]" in search_element:
        pass
    if "[" in search_element:
        pass
    while True:
        if search_element in open(file_name, "r").readlines()[from_line]:
            break
        else:
            from_line = from_line + 1
    return from_line

print(acc_file_search("example.cfg", "raw_command"))