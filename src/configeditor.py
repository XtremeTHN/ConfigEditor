import simple_term_menu
from modules.parser import Parser

class ConfigEditor:
    def __init__(self, parser: Parser, file: str = None):
        self.file = file
        self.file_content = file.read() if file is not None else None

    def set_file(self, file):
        self.file = open(file, 'w+')
        self.file_content = self.file.read()
    
    def 
