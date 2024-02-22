from simple_term_menu import TerminalMenu
from modules.style import bold, underlined

class FormatDictionary:
    def __init__(self):
        self.msg = ""

    def columnize(self, dictionary):
        if isinstance(dictionary, dict):
            for clave, valor in dictionary.items():
                if isinstance(valor, dict):
                    self.columnize(valor)
                else:
                    self.msg = self.msg + f"{bold(clave)}: {valor}\n"
            msg = self.msg
            self.msg = ""
            return msg
        else:
            return bold(dictionary)

class Menu:
    def __init__(self, configs:dict):
        self.configs = configs
        self.update()
        self.history = [self.configs]
        self.fmt = FormatDictionary()

    def change_value(self, key, value: str | bool | list):
        self.configs[key] = value

    def get_choice(self):
        if (n:=self.term.show()) is not None:
            return list(self.configs)[n]
        else:
            self.configs = self.history[-1]
            try:
                self.history.pop()
            except:
                return
            self.update()
            return

    def get_value(self, key):
        if (n:=self.configs.get(key)) is None:
            return "No value"
        else:
            return self.fmt.columnize(n)
    
    def update(self):
        self.term = TerminalMenu(list(self.configs), preview_command=self.get_value, preview_size=0.75)

    def show(self):
        while True:
            if len(self.history) == 0:
                break
            choice = self.get_choice()
            if choice is None:
                continue
            if type(self.configs[choice]) == dict:
                self.history.append(self.configs)
                self.configs = self.configs[choice]
                self.update()

