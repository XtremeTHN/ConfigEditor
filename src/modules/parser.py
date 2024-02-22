import os
import pathlib
import json

import importlib.util

from modules.style import error, warn, Format

PARSER_SHARE_PATH=pathlib.Path(os.path.join(os.environ['HOME'], ".config", "configeditor"))
DEFAULT_PARSER_CONFIG={
    "parsers": [{}],
}
if PARSER_SHARE_PATH.exists() is False:
    PARSER_SHARE_PATH.mkdir(parents=True,exist_ok=True)

class Parser:
    filetype=""
    filename=""
    def __init__(self, file):
        ...

    def parse(self):
        ...


class UserParsers:
    def __init__(self):
        self.parser_conf_path = PARSER_SHARE_PATH / "parsers.json"
        if self.parser_conf_path.exists() is False:
            self.parser_conf_path.write_text(json.dumps(DEFAULT_PARSER_CONFIG))

        self.config = json.loads(self.parser_conf_path.read_text())
    
    def get_parser(self, name) -> Parser | None:
        for parser_conf in self.config["parsers"]:
            if (n:=parser_conf["name"]) == name:
               return self.load_parser_from_dict(parser_conf)
    
    def load_parser_from_dict(self, parser_conf: dict):
        base_path = PARSER_SHARE_PATH / "scripts"
        module_path = parser_conf.get("script")
        if module_path is None:
            module_path = PARSER_SHARE_PATH / "scripts" / f"{n}.py"
        else:
            module_path = base_path / module_path

        spec = importlib.util.spec_from_file_location(n, module_path)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except FileNotFoundError:
            error(f'"{module_path}" does not exist, if this is not the path of the script, you will need to specify the path on config')
        parser_obj: Parser = getattr(module, "Parser")
        if parser_obj is None:
            warn("The module", n, "doesn't have the class Parser")
            return
        if parser_conf.get("file") is None:
            error("Parser", n, "has no file section on the parsers.conf")
        if parser_conf["file"].get("name") is None:
            error("Parser has the file section incomplete, missing name key on file")
        if parser_conf["file"].get("type") is None:
            error("Parser", n, "has the file section incomplete, missing type key")

        parser_obj.filename = parser_conf["file"]["name"]
        parser_obj.filetype = parser_conf["file"]["type"]
                
        return parser_obj

    def print_parsers(self):
        print(f"{Format.underline + Format.bold}Available parsers:{Format.end}")
        for parser_conf in self.config["parsers"]:
            if (name:=parser_conf.get("name")) is not None:
                print(f"\t{name}")
            else:
                print("\tNo parser name")
