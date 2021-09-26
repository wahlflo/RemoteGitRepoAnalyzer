from git_index_parser import GitIndexFile, GitIndexFileEntry
from ..extension_to_importance import EXTENSION_TO_IMPORTANCE
from cli_formatter.output_formatting import colorize_string, Color


def show_file_extensions(index_file: GitIndexFile) -> None:
    entry: GitIndexFileEntry

    extension_set = set()
    for entry in index_file.get_entries():
        extension = entry.name.split('/')[-1].split('.')[-1]
        extension_set.add(extension)

    for extension in extension_set:
        importance = EXTENSION_TO_IMPORTANCE.get(extension, None)
        if importance is None:
            print(extension)
        elif importance == 0:
            print(colorize_string(color=Color.GREEN, text=extension))
        elif importance == 1:
            print(colorize_string(color=Color.YELLOW, text=extension))
        elif importance == 2:
            print(colorize_string(color=Color.MAGENTA, text=extension))
        elif importance == 3:
            print(colorize_string(color=Color.RED, text=extension))
