# RemoteGitRepoAnalyzer

A cli script analyze the content of a remote git repository, or a local index file.

## Installation

Install the package with pip

    pip3 install git+https://github.com/wahlflo/RemoteGitRepoAnalyzer

## Usage
Type ```remoteGitRepoAnalyzer --help``` to view the help.

```
usage: remoteGitRepoAnalyzer INPUT ACTION [OPTIONS]...

A cli script analyze the content of a remote git repo or a local index file

optional arguments:
  -u URL, --url URL     INPUT: URL to remote git repository
  -i FILE_PATH, --index FILE_PATH
                        INPUT: Path to local index file
  -h, --help            prints the help text
  -s, --structure       ACTION: prints out all checked in files in the repo
  -e, --file_extensions
                        ACTION: prints out all file_extensions of files in the repo
  --files               ACTION: prints out important files in the repo (with -v all files)
  --gitignore           ACTION: Shows the gitignore file
  --config              ACTION: Shows the config file
  --assessment          ACTION: Analyzes the content of the repo to find interesting files or configs (default action)
  --logs                ACTION: Shows the commit logs of the current branch
  --useragent USERAGENT
                        OPTION: overrides the default user agent
  --store               OPTION: store the files which have been downloaded
  -v, --verbose         OPTION: verbose mode, shows also unimportant files etc.
```

## Examples 


### Examples 1
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

### Examples 2
```
remoteGitRepoAnalyzer -u https://example.com:443/.git/config --structure
REPOSITORY
|-- .gitignore
|-- config.conf
|-- README.md
|-- .idea/
|   |-- dapi_web.iml
|   |-- modules.xml
|   |-- vcs.xml
|   |-- workspace.xml
|-- source/
|   |-- composer.json
```


### Examples 3
```
remoteGitRepoAnalyzer -u https://example.com:443/.git/config --logs
0000000000000000000000000000000000000000 8ba16761840bff3124eda5f33361cbed3b29a688 root <root@asdkljasd.(none)> 25.03.2019 18:53 +0000 clone: from https://github.com/userabc/abcde.git
8ba16761840bff3124eda5f33361cbed3b29a688 23af0ef2483f53ae2d2d6b9b947f29e3a679dc68 root <root@asdkljasd.(none)> 25.03.2019 21:55 +0000 commit: removed credentials from repository
```