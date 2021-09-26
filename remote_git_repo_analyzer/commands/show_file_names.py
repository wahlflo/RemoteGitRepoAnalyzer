from git_index_parser import GitIndexFile, GitIndexFileEntry
from ..extension_to_importance import EXTENSION_TO_IMPORTANCE
from cli_formatter.output_formatting import colorize_string, Color


def show_file_names(index_file: GitIndexFile, verbose: bool) -> None:
    entry: GitIndexFileEntry
    for entry in index_file.get_entries():
        extension = entry.name.split('/')[-1].split('.')[-1].lower()
        importance = EXTENSION_TO_IMPORTANCE.get(extension, None)
        if importance is None:
            print(entry.name)
        elif importance == 0 and verbose:
            print(colorize_string(color=Color.GREEN, text=entry.name))
        elif importance == 1 and verbose:
            print(colorize_string(color=Color.MAGENTA, text=entry.name))
        elif importance == 2:
            print(colorize_string(color=Color.YELLOW, text=entry.name))
        elif importance == 3:
            print(colorize_string(color=Color.RED, text=entry.name))
