from git_index_parser import GitIndexFile, GitIndexFileEntry
from ..extension_to_importance import estimate_importance_of_file, Importance
from cli_formatter.output_formatting import colorize_string, Color


def show_file_names(index_file: GitIndexFile, verbose: bool) -> None:
    entry: GitIndexFileEntry
    for entry in index_file.get_entries():

        importance = estimate_importance_of_file(filepath=entry.name)

        if importance == Importance.unimportant and verbose:
            print(colorize_string(color=Color.GREEN, text=entry.name))
        elif importance == Importance.normal and verbose:
            print(colorize_string(color=Color.MAGENTA, text=entry.name))
        elif importance == Importance.maybe_interesting:
            print(colorize_string(color=Color.YELLOW, text=entry.name))
        elif importance == Importance.certain_interesting:
            print(colorize_string(color=Color.RED, text=entry.name))
