import enum


class ImportanceModifier(enum.Enum):
    decrease = -1
    no_change = 0
    increase = 1


class Importance(enum.Enum):
    unimportant = 0
    normal = 1
    maybe_interesting = 2
    certain_interesting = 3


def estimate_importance_of_file_extension(extension: str) -> Importance:
    return {
        'jpg': Importance.unimportant,
        'png': Importance.unimportant,
        'js': Importance.unimportant,
        'css': Importance.unimportant,
        'ttf': Importance.unimportant,
        'scss': Importance.unimportant,
        'ico': Importance.unimportant,
        'svg': Importance.unimportant,
        'woff': Importance.unimportant,
        'woff2': Importance.unimportant,
        'less': Importance.unimportant,
        'gif': Importance.unimportant,
        'map': Importance.unimportant,
        'html': Importance.unimportant,
        'htm': Importance.unimportant,
        'psd': Importance.unimportant,
        'otf': Importance.unimportant,
        'eot': Importance.unimportant,
        'bmp': Importance.unimportant,
        'ufm': Importance.unimportant,
        'xcf': Importance.unimportant,
        'mustache': Importance.unimportant,
        'jpeg': Importance.unimportant,
        'ai': Importance.unimportant,
        'properties': Importance.unimportant,
        'cur': Importance.unimportant,
        'bcmap': Importance.unimportant,
        'LICENSE': Importance.unimportant,
        'feature': Importance.unimportant,
        'webmanifest': Importance.unimportant,

        'php': Importance.normal,
        'tpl': Importance.normal,
        'gitignore': Importance.normal,
        'phtml': Importance.normal,
        'md': Importance.normal,
        'txt': Importance.normal,

        'eml': Importance.maybe_interesting,
        'msg': Importance.maybe_interesting,
        'ppt': Importance.maybe_interesting,
        'pptx': Importance.maybe_interesting,
        'doc': Importance.maybe_interesting,
        'docx': Importance.maybe_interesting,
        'xls': Importance.maybe_interesting,
        'xlsx': Importance.maybe_interesting,
        'tar': Importance.maybe_interesting,
        'db': Importance.maybe_interesting,
        'sql': Importance.maybe_interesting,
        'ini': Importance.maybe_interesting,
        'gz': Importance.maybe_interesting,
        'json': Importance.maybe_interesting,
        'pdf': Importance.maybe_interesting,
        'zip': Importance.maybe_interesting,
        'log': Importance.maybe_interesting,
        'yml': Importance.maybe_interesting,
        'yaml': Importance.maybe_interesting,
        'htaccess': Importance.maybe_interesting,
        '': Importance.maybe_interesting,

        'htpasswd': Importance.certain_interesting,
        'key': Importance.certain_interesting,
        'conf': Importance.certain_interesting,
        'config': Importance.certain_interesting,
        'sh': Importance.certain_interesting,
        'cmd': Importance.certain_interesting,
        'bat': Importance.certain_interesting,
    }.get(extension, Importance.normal)


def estimate_importance_of_file_by_extension(filename: str) -> Importance:
    extension = _get_file_extension_from_filename(filename=filename)
    return estimate_importance_of_file_extension(extension=extension)


def estimate_importance_of_file(filepath: str) -> Importance:
    filepath = filepath.lower()
    split_filepath = filepath.split('/')

    filename = split_filepath[-1]

    importance_of_extension = estimate_importance_of_file_by_extension(filename=filename)
    importance_of_filename = _estimate_importance_of_file_by_name(filename=filename)

    importance = Importance(min(max(importance_of_extension.value + importance_of_filename.value, 0), 3))

    for directory_name in split_filepath:
        modifier = _estimate_importance_modifier_by_directory_name(directory_name=directory_name)
        importance = Importance(min(max(importance.value + modifier.value, 0), 3))

    return importance


def _estimate_importance_modifier_by_directory_name(directory_name: str) -> ImportanceModifier:
    return {
        'vendor': ImportanceModifier.decrease,
        'vendors': ImportanceModifier.decrease,
        'fonts': ImportanceModifier.decrease,
        'test': ImportanceModifier.decrease,
        'theme': ImportanceModifier.decrease,
        'themes': ImportanceModifier.decrease,
        'template': ImportanceModifier.decrease,
        'localization': ImportanceModifier.decrease,

        'conf': ImportanceModifier.increase,
        'config': ImportanceModifier.increase,
        'configuration': ImportanceModifier.increase,
        'logs': ImportanceModifier.increase,
        'certificate': ImportanceModifier.increase,
        'certificates': ImportanceModifier.increase,
    }.get(directory_name, ImportanceModifier.no_change)


def _estimate_importance_of_file_by_name(filename: str) -> ImportanceModifier:
    filename = '.'.join(filename.split('.')[:-1])
    for phrase in ['password', 'apikey', 'token', 'passwort', 'key', 'credential', 'confidential', 'config', 'conf']:
        if phrase in filename:
            return ImportanceModifier.increase
    return ImportanceModifier.no_change


def _get_file_extension_from_filename(filename: str):
    if '.' not in filename:
        return ''
    else:
        return filename.split('.')[-1]
