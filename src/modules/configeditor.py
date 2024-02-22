import os
from modules.parser import Parser, UserParsers
from modules.menu import Menu
from modules.style import error, warn, bold, underlined

class ConfigEditor:
    def __init__(self, file: str = ""):
        self.usr_parsers = UserParsers()
        self.file_name = file

        self.parser = None

    def set_file(self, file):
        self.file = open(file, 'w+')
        self.file_content = self.file.read()
    
    def detect(self):
        for parser in self.usr_parsers.config["parsers"]:
            if parser["file"]["name"] == "*":
                if os.path.splitext(self.file_name)[1] == parser["file"]["type"]:
                    print(f'Using parser "{parser["name"]}"')
                    self.parser = self.usr_parsers.load_parser_from_dict(parser)
                    return

            prsr_file_name = [parser["file"]["name"], parser["file"]["name"]]
            if ".".join(prsr_file_name) == os.path.split(self.file_name)[1]:
                print(f'Using parser "{parser["name"]}"')
                self.parser = self.usr_parsers.load_parser_from_dict(parser)
                return
        warn("Couldn't choose a suitable Parser. No parser was selected automatically")
    
    def show_menu(self): 
        if self.file_name == "":
            error("File is None")
        if self.parser is None:
            error("No parser has been selected.")
        
        configs: dict = self.parser(self.file_name).parse()
        if len(list(configs)) < 1:
            warn("Config file is empty")
            return
        
        print(underlined(bold("Select and change from the list below")))
        menu = Menu(configs)
        menu.show()
