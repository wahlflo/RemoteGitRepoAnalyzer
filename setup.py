import setuptools

with open('README.md', mode='r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()


setuptools.setup(
    name="remote_git_repo_analyzer",
    version="2.0.5",
    author="Florian Wahl",
    author_email="florian.wahl.developer@gmail.com",
    description="A cli script analyze the content of a remote git repo or a local index file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wahlflo/RemoteGitRepoAnalyzer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    install_requires=[
        'cli-formatter>=1.2.0',
        'git_index_parser>=1.0.0',
        'urllib3',
        'requests'
    ],
    entry_points={
        "console_scripts": [
            "remoteGitRepoAnalyzer=remote_git_repo_analyzer.cli_script:main"
        ],
    }
)
