from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *


root = Tk()
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu, tearoff=FALSE)
helpmenu = Menu(menu, tearoff=FALSE)
ACC = Menu(menu, tearoff=FALSE)

active_window = ""


def info():
    info = Tk()

    info.title("Info")
    info.resizable(width=0, height=0)

    text = """Aion Command Creator
    Version 1.0
    
    Offizielles Programm zum erstellen von eigenen Befehlen für die Aion Platform"""

    Label(info, text=text).pack()

    info.mainloop()


def command_window():
    def start_config_creator():
        global root
        global menu
        global filemenu
        global helpmenu
        global ACC
        root.destroy()
        root = Tk()
        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu, tearoff=FALSE)
        helpmenu = Menu(menu, tearoff=FALSE)
        ACC = Menu(menu, tearoff=FALSE)
        config_window()

    def anwser_extension():
        global global_answer
        global active_window
        active_window = "answer_extension"

        try:
            for variable in global_command:
                variable.destroy()
        except:
            pass

        separator = Frame(height=2, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=5)

        answer_extension_choose = Combobox(root, values=["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaggggggggggnjmrjrzhzaaaaaaaaaaaaa", "b"], width=100)
        answer_extension_choose.pack()
        answer_extension_choose.current(0)

        free_space = Label(root)
        free_space.pack()

        answer = Text(root, width=80, height=5)
        answer.pack()

        global_answer = [separator, answer_extension_choose, free_space, answer]

    def own_command():
        global global_command
        global active_window
        active_window = "own_command"

        try:
            for variable in global_answer:
                variable.destroy()
        except:
            pass

        separator = Frame(height=2, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=5)



        global_command = [separator]

    def command_event(event):
        global active_window
        if command_choose.get() == "----------------------------":
            new()
            active_window = ""
        elif command_choose.get() == "Antwort Erweiterung":
            if active_window == "answer_extension":
                pass
            else:
                anwser_extension()
        elif command_choose.get() == "Eigener Befehl":
            if active_window == "own_command":
                pass
            else:
                own_command()

    def new():
        try:
            for variable in global_answer:
                variable.destroy()
        except:
            pass

        try:
            for variable in global_command:
                variable.destroy()
        except:
            pass

        command_choose.current(0)

    root.title("ACC | Aion Command Creator | command Creator")
    root.resizable(width=0, height=0)

    menu.add_cascade(label="Datei", menu=filemenu)
    filemenu.add_command(label="Neu", command=new)
    filemenu.add_command(label="Öffnen...")
    filemenu.add_command(label="Speichern")
    filemenu.add_command(label="Speichern unter...")
    filemenu.add_separator()
    filemenu.add_command(label="Beenden", command=root.destroy)
    menu.add_cascade(label="Hilfe", menu=helpmenu)
    helpmenu.add_command(label="Hilfe anzeigen")
    helpmenu.add_separator()
    helpmenu.add_command(label="Info", command=info)
    menu.add_cascade(label="ACC", menu=ACC)
    ACC.add_command(label="Zum config Creator", command=start_config_creator)

    Label(root, text="Was für eine Art soll dein Befehls sein?").pack()
    command_choose = Combobox(root, values=["----------------------------", "Antwort Erweiterung", "Eigener Befehl"])
    command_choose.pack()
    command_choose.current(0)
    command_choose.bind("<<ComboboxSelected>>", command_event)

    root.mainloop()

def config_window():

    def acc_file_search(file_name, search_element):
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
                    acc_file = ""
                    return acc_file
                elif search_element not in not_needed_informations:
                    acc_file = ""
                    return acc_file
                else:
                    acc_file = ""
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

    def start_command_creator():
        global root
        global menu
        global filemenu
        global helpmenu
        global ACC
        root.destroy()
        root = Tk()
        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu, tearoff=FALSE)
        helpmenu = Menu(menu, tearoff=FALSE)
        ACC = Menu(menu, tearoff=FALSE)
        command_window()

    def create_acc_config():
        name = name_entry.get()
        author = author_entry.get()
        version = version_entry.get()
        command_type = command_type_entry.get()
        command_file = command_file_entry.get()
        raw_command = raw_command_scrolledtext.get(1.0, END)
        new_file = filedialog.asksaveasfile(mode="w", defaultextension=".cfg", filetypes=(("CFG Datei", "*.cfg"),))
        global new_file_name
        new_file_name = new_file.name
        new_file.write(
            'name=' + name + '\nauthor=' + author + '\nversion=' + version + '\ncommand_type=' + command_type + '\ncommand_file=["' + command_file + '"]\nraw_command=["' + raw_command + '"]')

    def get_def():
        get_def_list = []
        numbers = []
        def_print = open(open_command_file_name, "r").read().splitlines()
        with open(open_command_file_name, "r") as get_def:
            for line in get_def:
                if "def " in line:
                    def_line = line
                    numbers.append(def_print[acc_search_file_element(open_command_file_name, def_line)])
        for space in numbers:
            non_space = space.lstrip()
            get_def_list.append(non_space)
        raw_command_scrolledtext.config(state=NORMAL)
        for insert in get_def_list:
            raw_command_scrolledtext.insert(1.0, insert + " = '',\n")

    def new():
        get_function.config(state=DISABLED)
        name_entry.delete(0, END)
        author_entry.delete(0, END)
        version_entry.delete(0, END)
        command_type_entry.delete(0, END)
        command_file_entry.delete(0, END)
        raw_command_scrolledtext.delete(1.0, END)

    def open_acc_config():
        open_file = filedialog.askopenfile(filetypes=(("CFG Datei", "*.cfg"), ("Alle Dateien", "*.*")))
        global open_file_name
        open_file_name = open_file.name
        if ".cfg" not in open_file_name:
            messagebox.showerror("Aion Command Creator", "Die Ausgewählte Datei ist keine config (*.cfg) Datei")
        else:
            open_file_read = open(open_file_name, "r").read()
            if "name=" and "version=" and "command_type=" and "command_file=" and "raw_command=" in open_file_read:
                raw_command_scrolledtext.config(state=NORMAL)
                name_entry_insert = acc_file_search(open_file_name, "name")
                author_entry_insert = acc_file_search(open_file_name, "author")
                version_entry_insert = acc_file_search(open_file_name, "version")
                command_type_entry_insert = acc_file_search(open_file_name, "command_type")
                command_file_entry_insert = acc_file_search(open_file_name, "command_file")
                raw_command_scrolledtext_insert = acc_file_search(open_file_name, "raw_command")
                raw_command_scrolledtext_insert = raw_command_scrolledtext_insert.replace(",", "\n")
                raw_command_scrolledtext_insert = raw_command_scrolledtext_insert.replace(" ", "")
                name_entry.delete(0, END)
                name_entry.insert(0, name_entry_insert)
                author_entry.delete(0, END)
                author_entry.insert(0, author_entry_insert)
                version_entry.delete(0, END)
                version_entry.insert(0, version_entry_insert)
                command_type_entry.delete(0, END)
                command_type_entry.insert(0, command_type_entry_insert)
                command_file_entry.delete(0, END)
                command_file_entry.insert(0, command_file_entry_insert)
                raw_command_scrolledtext.delete(1.0, END)
                raw_command_scrolledtext.insert(1.0, raw_command_scrolledtext_insert)
            else:
                print(open_file.name + " kann nicht gelesen werden")

    def open_command_file():
        import ntpath
        open_file = filedialog.askopenfile(filetypes=(("PY Datei", "*.py"), ("Alle Dateien", "*.*")))
        global open_command_file_name
        open_command_file_name = open_file.name
        if ".py" not in open_command_file_name:
            messagebox.showerror("Aion Command Creator", "Die Ausgewählte Datei ist keine Python (*.py) Datei")
        else:
            command_file_entry.delete(0, END)
            command_file_entry.insert(0, ntpath.basename(open_file.name))
            raw_command_scrolledtext.config(state=NORMAL)
            get_function.config(fg="green", state=NORMAL)

    def save():
        global file_name
        try:
            file_name = open_file_name
        except:
            try:
                file_name = new_file_name
            except:
                create_acc_config()
                return
        name = name_entry.get()
        author = author_entry.get()
        version = version_entry.get()
        command_type = command_type_entry.get()
        command_file = command_file_entry.get()
        raw_command = raw_command_scrolledtext.get("1.0", END)
        file = open(file_name, "w")
        file.write('name=' + name + '\nauthor=' + author + '\nversion=' + version + '\ncommand_type=' + command_type + '\ncommand_file=["' + command_file + '"]\nraw_command=["' + raw_command + '"]')

    def show_help():
        help = Tk()

        help.title("Hilfe anzeigen")
        help.resizable(width=0, height=0)

        Label(help, text="Hilfe zum Aion Command Creator im Bereich 'config Creator'\n\n").pack()
        Label(help, text="'Befehlspaket' = Paket, worin sich alle Dateien befinden").pack()
        Label(help, text="'/' = oder").pack()
        Label(help, text="Name: ").pack()
        name = Text(help, height=2, width=100)
        name.insert(1.0, "Legt den Namen für das Befehlspaket fest\n"
                         "Bsp: Tiergeräusche -> geräusche.py(Datei mit den Befehlsnamen) + geräusche.cfg(Konfigurations Datei)")
        name.config(state=DISABLED)
        name.pack()
        Label(help, text="Autor").pack()
        author = Text(help, height=2, width=100)
        author.insert(1.0, "Legt den Namen vom Autor des Befehlspaket fest\n"
                           "Bsp: xXauthorXx / CaCtUsFiGhTeR")
        author.config(state=DISABLED)
        author.pack()
        Label(help, text="Version").pack()
        version = Text(help, height=2, width=100)
        version.insert(1.0, "Legt die Version vom Befehlspaket fest\n"
                            "Bsp: v.1.1 / 1.3.7.4")
        version.config(state=DISABLED)
        version.pack()
        Label(help, text="Befehls Typ").pack()
        command_type = Text(help, height=2, width=100)
        command_type.insert(1.0, "Legt den Befehlstyp des Befehlspaket fest\n"
                                 "Bsp: Spiel / Antwort Erweiterung")
        command_type.config(state=DISABLED)
        command_type.pack()
        Label(help, text="Befehlsdatei").pack()
        command_file = Text(help, height=2, width=100)
        command_file.insert(1.0, "Legt die Datei mit den Befehlen fest\n"
                                 "Bsp: geräusche.py -> def kuh(): (enthält z.B. den Code zum abspielen von einem Kuh Geräusch)")
        command_file.config(state=DISABLED)
        command_file.pack()
        Label(help, text="Befehl(e)").pack()
        raw_command = Text(help, height=2, width=100)
        raw_command.insert(1.0, "Legt den Namen der Funktion fest und mit welchen Spracheingaben diese aufgerufen wird\n"
                                "Bsp: def kuh(): = 'Mach Kuh Geräusche'")
        raw_command.config(state=DISABLED)
        raw_command.pack()

    root.title("ACC | Aion Command Creator | config Creator")
    root.resizable(width=0, height=0)

    menu.add_cascade(label="Datei", menu=filemenu)
    filemenu.add_command(label="Neu", command=new)
    filemenu.add_command(label="Öffnen...", command=open_acc_config)
    filemenu.add_command(label="Speichern", command=save)
    filemenu.add_command(label="Speichern unter...", command=create_acc_config)
    filemenu.add_separator()
    filemenu.add_command(label="Beenden", command=root.destroy)
    menu.add_cascade(label="Hilfe", menu=helpmenu)
    helpmenu.add_command(label="Hilfe anzeigen", command=show_help)
    helpmenu.add_separator()
    helpmenu.add_command(label="Info", command=info)
    menu.add_cascade(label="ACC", menu=ACC)
    ACC.add_command(label="Zum command Creator", command=start_command_creator)

    Label(root, text="* = Wird nicht unbedingt benötigt").pack()

    Label(root, text="Name:", font="Times").pack()
    name_entry = Entry(root, width=40)
    name_entry.pack()

    Label(root, text="Autor*:", font="Times").pack()
    author_entry = Entry(root, width=40)
    author_entry.pack()

    Label(root, text="Version*: ", font="Times").pack()
    version_entry = Entry(root, width=40)
    version_entry.pack()

    Label(root, text="Befehls Typ*:", font="Times").pack()
    command_type_entry = Entry(root, width=40)
    command_type_entry.pack()

    Label(root, text="Befehls Datei:", font="Times").pack()
    command_file_entry = Entry(root, width=55)
    command_file_entry.pack()

    Button(root, text="Wähle Datei aus", command=open_command_file).pack()
    get_function = Button(root, text="Versuche alle Befehle aufzulisten", command=get_def)
    get_function.config(state=DISABLED)
    get_function.pack()

    Label(root, text="Befehl(e):", font="Times").pack()
    raw_command_scrolledtext = scrolledtext.ScrolledText(root, height=15, width=50)
    raw_command_scrolledtext.config(state=DISABLED)
    raw_command_scrolledtext.pack()

    root.mainloop()


command_window()