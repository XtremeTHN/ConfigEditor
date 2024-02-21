from modules.parser import UserParsers
import icecream
user = UserParsers()
user.list_parsers()

parser = user.get_parser("hyprland")

print(parser.filetype, parser.filename)
