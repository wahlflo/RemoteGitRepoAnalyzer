from git_index_parser import GitIndexParser, GitIndexParserException
import argparse
from cli_formatter.output_formatting import colorize_string, Color, error, warning, info
from remote_git_repo_analyzer.commands import show_file_structure, show_file_names, show_file_extensions
import requests
import io
import urllib3

from remote_git_repo_analyzer.extension_to_importance import EXTENSION_TO_IMPORTANCE

urllib3.disable_warnings()

USERAGENT = ''
STORE_FILES = False


def download(url: str, return_string: bool = False) -> io.BytesIO or str or None:
    try:
        try:
            response = requests.get(url=url, headers={'User-Agent': USERAGENT}, verify=True)
        except requests.exceptions.SSLError:
            response = requests.get(url=url, headers={'User-Agent': USERAGENT}, verify=False)
            warning('The remote certificate is not trusted')
    except:
        error('The URL "{}" could not be downloaded'.format(url))
        return None

    if response.status_code != 200:
        error('The URL "{}" could not be downloaded'.format(url))
        return None

    if STORE_FILES:
        filename = url.split('/')[-1]
        with open('gitRepoAnalyzer_{}'.format(filename), mode='wb') as outout:
            outout.write(response.content)

    if return_string:
        return response.text
    else:
        return io.BytesIO(response.content)


class Finding:
    def __init__(self, level: int, message: str, value: str):
        self.level = level
        self.message = message
        self.value = value


def make_assessment(url_to_repo: str):
    findings = list()

    # Analyze the config file
    url_to_config = url_to_repo + '.git/config'
    info('analyze the config file: "{}"'.format(url_to_config))
    config_file = download(url=url_to_config, return_string=True)
    if config_file is not None:
        config_file = config_file.replace('\t', '').replace(' ', '')
        for line in config_file.split('\n'):
            if line.startswith('url='):
                url = line[4:]
                new_url = url.replace('http://', '')
                new_url = new_url.replace('https://', '')
                new_url = new_url.replace('ssh://', '')
                if '@' in new_url:
                    username_plus_password = new_url.split('@')[0]
                    findings.append(Finding(level=1, message='URL of the repository origin', value=url.split('@')[1]))
                    if ':' in username_plus_password:
                        username = username_plus_password.split(':')[0]
                        findings.append(Finding(level=3, message='username and password are included in the config file', value=username_plus_password))
                    else:
                        findings.append(Finding(level=1, message='username of the git user', value=username_plus_password))
                else:
                    findings.append(Finding(level=1, message='URL of the repository origin', value=url))

    # Analyze
    url_to_index_file = url_to_repo + '.git/index'
    info('analyze the index file: "{}"'.format(url_to_index_file))
    index_file = download(url=url_to_index_file)
    if index_file is not None:
        index_file = GitIndexParser.parse(file=index_file)
        for entry in index_file.get_entries():
            extension = entry.name.split('/')[-1].split('.')[-1]
            importance = EXTENSION_TO_IMPORTANCE.get(extension, None)
            if importance == 0 or importance == 1:
                pass
            elif importance == 2:
                findings.append(Finding(level=2, message='interesting file found', value=entry.name))
            elif importance == 3:
                findings.append(Finding(level=3, message='interesting file found', value=entry.name))
            else:
                for phrase in ['password', 'apikey', 'token', 'passwort', 'key', 'credential', 'confidential', 'config']:
                    if phrase in entry.name:
                        findings.append(Finding(level=2, message='interesting filename found', value=entry.name))

    # Analyze the README.md
    url_to_readme_file = url_to_repo + 'README.md'
    info('analyze the README.md file: "{}"'.format(url_to_readme_file))
    readme_file = download(url=url_to_readme_file, return_string=True)
    if readme_file is not None:
        readme_file = readme_file.lower()
        for phrase in ['password', 'api-key', 'apikey', 'token', 'passwort', 'key', 'credential', 'confidential']:
            if phrase in readme_file:
                findings.append(Finding(level=2, message='the phrase "{}" occurred in the README.md file'.format(phrase), value=url_to_readme_file))

    # Analyze the .gitignore file
    url_to_gitignore = url_to_repo + '.gitignore'
    info('analyze the gitignore file: "{}"'.format(url_to_gitignore))
    gitignore = download(url=url_to_gitignore, return_string=True)
    if gitignore is not None:
        gitignore = gitignore.lower()
        for phrase in ['.htaccess', 'nginx.conf', 'conf', 'token', 'uploads', '.key', '.pem']:
            if phrase in gitignore:
                findings.append(Finding(level=2, message='the phrase "{}" occurred in the gitignore file'.format(phrase), value=url_to_gitignore))

    info('found {} findings.'.format(len(findings)))
    if len(findings) == 0:
        return

    print(60*'#')

    finding: Finding
    for finding in findings:
        if finding.level == 1:
            print('[*] {}: {}'.format(finding.message, colorize_string(color=Color.BLUE, text=finding.value)))
        elif finding.level == 2:
            print('[+] {}: {}'.format(finding.message, colorize_string(color=Color.MAGENTA, text=finding.value)))
        else:
            print('[!] {}: {}'.format(finding.message, colorize_string(color=Color.RED, text=finding.value)))


def main():
    global USERAGENT, STORE_FILES

    parser = argparse.ArgumentParser(usage='remoteGitRepoAnalyzer [OPTION]...', description='A cli script analyze the content of a remote git repo or a local index file', add_help=False)
    parser.add_argument('-u', '--url', dest="url", help="URL to remote git repository", type=str, default=None)
    parser.add_argument('-i', '--index', dest="file_path", help="Path to local index file - prints out all checked in files in the repo", type=str, default=None)
    parser.add_argument('-h', '--help', dest='help', help="prints the help text", action='store_true', default=False)
    parser.add_argument('-s', '--structure', dest='structure', help="prints out all checked in files in the repo", action='store_true', default=False)
    parser.add_argument('-e', '--file_extensions', dest='file_extensions', help="prints out all file_extensions of files in the repo", action='store_true', default=False)
    parser.add_argument('--files', dest='files', help="prints out all files in the repo", action='store_true', default=False)
    parser.add_argument('--useragent', dest='useragent', help="overrides the default user agent", type=str, default='RemoteGitRepoAnalyzer')
    parser.add_argument('--gitignore', dest='gitignore', help="Shows the gitignore file", action='store_true', default=False)
    parser.add_argument('--config', dest='config', help="Shows the config file", action='store_true', default=False)
    parser.add_argument('--assessment', dest='assessment', help="Analyzes the content of the repo to find interesting files or configs", action='store_true', default=False)
    parser.add_argument('--store', dest='store_files', help="store the files which where downloaded", action='store_true', default=False)

    parsed_arguments = parser.parse_args()

    USERAGENT = parsed_arguments.useragent
    STORE_FILES = parsed_arguments.store_files

    if parsed_arguments.help:
        parser.print_help()
        return

    if parsed_arguments.url is None and parsed_arguments.file_path is None:
        error('you must either specify an URL or a filepath to a git repository')
        return

    if parsed_arguments.url is not None and parsed_arguments.file_path is not None:
        error('you must either specify an URL or a filepath to a git repository but you can not specify both')
        return

    if parsed_arguments.file_path:
        try:
            index_file = GitIndexParser.parse_file(path_to_file=parsed_arguments.file_path)
        except GitIndexParserException as exception:
            error('The index file could not be parsed: {}'.format(exception.message))
            return
        if parsed_arguments.structure:
            show_file_structure(index_file=index_file)
        elif parsed_arguments.files:
            show_file_names(index_file=index_file)
        elif parsed_arguments.file_extensions:
            show_file_extensions(index_file=index_file)
        return

    url: str = parsed_arguments.url
    url_to_repo = url.split('.git')[0]

    if parsed_arguments.structure:
        url_to_index_file = url_to_repo + '.git/index'
        index_file = download(url=url_to_index_file)
        if index_file is not None:
            index_file = GitIndexParser.parse(file=index_file)
            show_file_structure(index_file=index_file)

    elif parsed_arguments.files:
        url_to_index_file = url_to_repo + '.git/index'
        index_file = download(url=url_to_index_file)
        if index_file is not None:
            index_file = GitIndexParser.parse(file=index_file)
            show_file_names(index_file=index_file)

    elif parsed_arguments.file_extensions:
        url_to_index_file = url_to_repo + '.git/index'
        index_file = download(url=url_to_index_file)
        if index_file is not None:
            index_file = GitIndexParser.parse(file=index_file)
            show_file_extensions(index_file=index_file)

    elif parsed_arguments.gitignore:
        url_to_gitignore = url_to_repo + '.gitignore'
        gitignore_file = download(url=url_to_gitignore, return_string=True)
        print(gitignore_file)
    elif parsed_arguments.config:
        url_to_config = url_to_repo + '.git/config'
        config_file = download(url=url_to_config, return_string=True)
        print(config_file)

    elif parsed_arguments.assessment:
        make_assessment(url_to_repo=url_to_repo)


if __name__ == '__main__':
    main()
