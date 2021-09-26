from git_index_parser import GitIndexFile, GitIndexFileEntry


class FileStructureTree:
    def __init__(self, name: str = None, level=-1):
        self.name = name
        self.level = level
        self.entries = list()
        self.child_trees = list()

    def add(self, names: list, entry: GitIndexFileEntry):
        next_name = names.pop(0)
        if len(names) == 0:
            self.entries.append(FileStructureLeaf(name=next_name, entry=entry, level=self.level+1))
        else:
            found = False
            for child in self.child_trees:
                if child.name == next_name:
                    child.add(names=names, entry=entry)
                    found = True
                    break
            if not found:
                new_tree = FileStructureTree(name=next_name, level=self.level+1)
                self.child_trees.append(new_tree)
                new_tree.add(names=names, entry=entry)

    def show(self):
        if self.level > 0:
            print('|', end='')
            print(self.level * '   ', end='')
            print('|--', self.name+'/')
        elif self.level == 0:
            print('|--', self.name + '/')
        else:
            print('REPOSITORY')

        for x in self.entries:
            x.show()
        for x in self.child_trees:
            x.show()


class FileStructureLeaf:
    def __init__(self, name: str, entry: GitIndexFileEntry, level: int):
        self.name = name
        self.entry = entry
        self.level = level

    def show(self):
        if self.level > 0:
            print('|', end='')
            print(self.level * '   ', end='')
        print('|--', self.name)


def show_file_structure(index_file: GitIndexFile):
    tree = FileStructureTree()
    for entry in index_file.get_entries():
        tree.add(names=entry.name.split('/'), entry=entry)
    tree.show()
