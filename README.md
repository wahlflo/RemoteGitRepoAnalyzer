# RemoteGitRepoAnalyzer

A cli script analyze the content of a remote git repository, or a local index file.

## Installation

Install the package with pip

    pip install remote_git_repo_analyzer

## Usage
Type ```remoteGitRepoAnalyzer --help``` to view the help.

```
usage: remoteGitRepoAnalyzer [OPTION]...

A cli script analyze the content of a remote git repo or a local index file

optional arguments:
  -u URL, --url URL     URL to remote git repository
  -i FILE_PATH, --index FILE_PATH
                        Path to local index file - prints out all checked in files in the repo
  -h, --help            prints the help text
  -s, --structure       prints out all checked in files in the repo
  -e, --file_extensions
                        prints out all file_extensions of files in the repo
  --files               prints out all files in the repo
  --useragent USERAGENT
                        overrides the default user agent
  --gitignore           Shows the gitignore file
  --config              Shows the config file
  --assessment          Analyzes the content of the repo to find interesting files or configs
  --store               store the files which have been downloaded
  -v, --verbose         verbose mode: shows also unimportant files etc.
```

## Example

```
remoteGitRepoAnalyzer -u https://example.com:443/.git/config --assessment
[+] analyze the config file: "https://example.com:443/.git/config"
[!] The remote certificate is not trusted
[+] analyze the index file: "https://example.com:443/.git/index"
[!] The remote certificate is not trusted
[+] analyze the README.md file: "https://example.com:443/README.md"
[!] The remote certificate is not trusted
[!] The URL "https://rootca-s.allianz.com:443/README.md" could not be downloaded
[+] analyze the gitignore file: "https://example.com:443/.gitignore"
[!] The remote certificate is not trusted
[+] found 7 findings.
############################################################
[*] URL of the repository origin: gitlab.example.com:Hak/test_repo.git
[!] username and password are included in the config file: bob:SecurePassword
[!] interesting file found: config/certificate.key
[+] the phrase "confidential" occurred in the README.md file: https://example.com:443/README.md
```
