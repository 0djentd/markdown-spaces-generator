import re
import sys

from typing import List, Optional

from markdown_spaces_generator import __version__

import click


def check_if_stop_line(line) -> bool:
    stop_lines_re = ["^$", "^\s*#"]
    for expr in stop_lines_re:
        if re.match(expr, line):
            return True
    return False


def add_spaces(lines: List[str]) -> List[str]:
    result = []
    lines_shift: List[Optional[str]] = [None]
    lines_shift += lines[:-1]

    for line, previous_line in zip(lines, lines_shift):
        if previous_line is not None:
            if not check_if_stop_line(previous_line):
                if not check_if_stop_line(line):
                    result += [previous_line + "  "]
                    continue
            result += [previous_line]

    result += [lines[-1]]
    return result


def read_file(filename) -> List[str]:
    lines = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    return lines


def write_file(filename, lines):
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines([x + "\n" for x in lines])


def process_file(filename: str, replace: bool):
    lines = read_file(filename)
    result = add_spaces(lines)
    if replace:
        write_file(filename, result)
    else:
        for line in result:
            print(line)


@click.command()
@click.argument("files", nargs=-1)
@click.option("--replace/--no-replace", default=False)
@click.version_option(__version__)
def main(files, replace):
    if len(files) == 0:
        sys.exit(1)
    for file in files:
        process_file(file, replace)


if __name__ == "__main__":
    main()
