#=================================================================
# Author: Juan Jose Solorzano Carrillo
# Email: juanjose.solorzano.c@gmail.com
# Data: 13/06/2026
#=================================================================

import sys
import msvcrt
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import TerminalTrueColorFormatter
from os.path import exists, getsize, isfile, isdir
from colored import Fore, Style
import shutil

PINK =   Fore.rgb("100%", "0%", "60%") 
VIOLET = Fore.rgb("30%", "10%", "100%")
GRAY = Fore.rgb("50%", "50%", "50%")
SEPARATOR = '─' * 100
SEPARATOR_2 = '═' * 100
TITLE = "{0}\n%s\n{0}"


# For Unix-like systems. 
#def wait_for_key(current, total):
#    fd = sys.stdin.fileno()
#    old = termios.tcgetattr(fd)
#    try:
#        tty.setraw(fd)
#        key = sys.stdin.read(1)
#    finally:
#        termios.tcsetattr(fd, termios.TCSADRAIN, old)
#    return key.lower() != 'q'

def get_terminal_height():
    return shutil.get_terminal_size().lines - 3  # leave room for status bar

def wait_for_key(current, total):
    """Display prompt and wait for Enter or Q key."""
    prompt = f"\033[7m -- {current}/{total} lines | Press [Enter] to continue, [Q] to quit -- \033[0m"
    print(prompt, end='', flush=True)
    while True:
        key = msvcrt.getwch()
        if key in ('\r', '\n'):       # Enter
            print('\r' + ' ' * len(prompt) + '\r', end='', flush=True)
            return True
        elif key.lower() == 'q':      # Quit
            print()
            return False

def is_binary(file_path):
    with open(file_path, 'rb') as f:
        chunk = f.read(1024)
        return b'\x00' in chunk

def bat_format(colorized_output, file_name, file_size):
    lines = colorized_output.splitlines()
    number_of_line = len(lines)
    name_colored = f"{PINK}{file_name} ({file_size} bytes) | {number_of_line} lines {Style.reset}"
    print(TITLE.format(SEPARATOR) % "    %s" % name_colored)

    max_digits = len(str(len(lines)))
    page_size = get_terminal_height()

    for i, (line, content) in enumerate(enumerate(lines, start=1), start=1):
        print(f"{GRAY}{line:>{max_digits}} │ {Style.reset}{content}")
        # Pause every page_size lines (except at the very last line)
        if i % page_size == 0 and i < number_of_line:
            if not wait_for_key(i, number_of_line):
                print(f"\n{PINK}: < INTERRUPTED >{Style.reset}")
                print(SEPARATOR_2)
                return

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
        bat_format(code_text[0], f"{file_name} <BINARY>", getsize(file_path))
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
    bat_format(colored_output, file_name, file_size)

def run():
    if len(sys.argv) != 2:
        print("Usage: batcat <file_path>", file=sys.stderr)
        sys.exit(1)
    target_file = sys.argv[1]
    colorize_file(target_file)

if __name__ == '__main__':
    run()