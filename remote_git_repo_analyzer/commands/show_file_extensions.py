from git_index_parser import GitIndexFile, GitIndexFileEntry
from ..extension_to_importance import estimate_importance_of_file_extension, Importance
from cli_formatter.output_formatting import colorize_string, Color


def show_file_extensions(index_file: GitIndexFile) -> None:
    entry: GitIndexFileEntry

    extension_set = set()
    for entry in index_file.get_entries():
        if '.' in entry.name:
            extension = entry.name.split('/')[-1].split('.')[-1]
            extension_set.add(extension)

    for extension in extension_set:
        importance = estimate_importance_of_file_extension(extension=extension)
        if importance == Importance.unimportant:
            print(colorize_string(color=Color.GREEN, text=extension))
        elif importance == Importance.normal:
            print(colorize_string(color=Color.MAGENTA, text=extension))
        elif importance == Importance.maybe_interesting:
            print(colorize_string(color=Color.YELLOW, text=extension))
        elif importance == Importance.certain_interesting:
            print(colorize_string(color=Color.RED, text=extension))
