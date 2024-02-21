import os
import pathlib
import json

import importlib.util

PARSER_SHARE_PATH=pathlib.Path(os.path.join(os.environ['HOME'], ".config", "configeditor"))
DEFAULT_PARSER_CONFIG={
    "parsers": [{}],
}
if PARSER_SHARE_PATH.exists() is False:
    PARSER_SHARE_PATH.mkdir(parents=True,exist_ok=True)

class Parser:
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
    
    def get_parser(self, name) -> Parser:
        for parsers_conf_dict in self.config['parsers']:
            for parser_conf in parsers_conf_dict:
                if (n:=parser_conf["name"]) == name:
                    spec = importlib.util.spec_from_file_location(n, parser_conf["path"])
                    module = importlib.util.module_from_spec(spec)

                    spec.loader.exec_module(module)

                    return module
