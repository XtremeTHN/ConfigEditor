from simple_term_menu import TerminalMenu
from modules.style import Format

class Menu:
    def __init__(self, configs:dict):
        self.configs = configs
        self.term = TerminalMenu(list(configs))
        self.history = [self.configs]

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
    
    def update(self):
        self.term = TerminalMenu(list(self.configs))

    def show(self):
        pos = 0
        while True:
            if len(self.history) == 0:
                break
            choice = self.get_choice()
            if choice is None:
                continue
            if type(self.configs[choice]) == dict:
                pos +=1
                self.history.append(self.configs)
                self.configs = self.configs[choice]
                print(self.configs)
                self.update()

