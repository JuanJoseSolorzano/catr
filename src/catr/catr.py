#=================================================================
# Author: Juan Jose Solorzano Carrillo
# Email: juanjose.solorzano.c@gmail.com
# Data: 13/06/2026
#=================================================================

import sys
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import TerminalTrueColorFormatter
from os.path import exists,getsize,isfile,isdir
from colored import Fore, Style

PINK =   Fore.rgb("100%", "0%", "60%") 
VIOLET = Fore.rgb("30%", "10%", "100%")
GRAY = Fore.rgb("50%", "50%", "50%")
SEPARATOR = '─' * 100
SEPARATOR_2 = '═' * 100
TITLE = "{0}\n%s\n{0}"

def is_binary(file_path):
    with open(file_path, 'rb') as f:
        chunk = f.read(1024)
        return b'\x00' in chunk

def bat_format(colorized_output,file_name,file_size):
    lines = colorized_output.splitlines()
    number_of_line = len(lines)
    name_colored = f"{PINK}{file_name} ({file_size} bytes) | {number_of_line} lines {Style.reset}"
    print(TITLE.format(SEPARATOR)%"    %s" % name_colored)
    max_digits = len(str(len(lines)))
    for line,content in enumerate(lines,start=1):
        print(f"{GRAY}{line:>{max_digits}} │ {Style.reset}{content}")
    print(SEPARATOR)
    print(f"{PINK}: < END OF FILE >{Style.reset}")
    print(SEPARATOR_2)

def colorize_file(file_path):
    if not exists(file_path):
        print(f"Error: File \"{file_path}\" not found.", file=sys.stderr)
        return 
    if not isfile(file_path) or isdir(file_path):
        print(f"{Fore.red}[ERROR] \"{file_path}\" is not a valid file to display.{Style.reset}")
        sys.exit(1)
    separator = '\\' if sys.platform.startswith('win') else '/'
    file_name = file_path.split(separator)[-1]
    if is_binary(file_path):
        with open(file_path, 'rb') as file:
            code_text = file.readlines()
        bat_format(code_text[0],f"{file_name} <BINARY>",getsize(file_path))
        return
    with open(file_path, 'r', encoding='utf-8') as file:
        code_text = file.read() 
    try:
        lexer = get_lexer_for_filename(file_path)
    except Exception:
        lexer = TextLexer()
    file_size = getsize(file_path)
    formatter = TerminalTrueColorFormatter(style='native')
    colored_output = highlight(code_text, lexer, formatter)
    bat_format(colored_output,file_name,file_size)

def run():
    # Capture command line arguments dynamically
    if len(sys.argv) != 2:
        print("Usage: batcat <file_path>", file=sys.stderr)
        sys.exit(1)
    target_file = sys.argv[1]
    colorize_file(target_file)
# Keeps compatibility for running the file directly with: python cat_cli.py
if __name__ == '__main__':
    run()
