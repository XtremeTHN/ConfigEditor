import sys

class Format:
    end = '\033[0m'
    underline = '\033[4m'
    bold = '\033[1m'

    class Colors:
        red = '\u001b[31m'
        light_red = "\033[1;31m"


def warn(*args):
    print(Format.Colors.light_red, *args, Format.end)

def error(*args, exit_code=1):
    print(Format.Colors.red, *args, Format.end)
    sys.exit(exit_code)

def bold(msg) -> str:
    return f"{Format.bold}{msg}{Format.end}"

def underlined(msg) -> str:
    return Format.underline + msg + Format.end
