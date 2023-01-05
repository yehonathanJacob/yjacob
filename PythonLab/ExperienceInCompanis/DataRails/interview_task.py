from __future__ import annotations

from typing import List


class File:
    def __init__(self, name: str, size: float):
        self.name = name
        self.size = size


class Folder:
    def __init__(self, name: str, content: List[Folder | File]):
        self.name = name
        self.content = content

    def get_size(self):
        if not self.content:
            return 0

        queue = self.content.copy()

        size = 0
        while queue:
            item = queue.pop()
            if isinstance(item, Folder):
                queue.extend(item.content)
            elif isinstance(item, File):
                size += item.size

        return size

    @property
    def size(self) -> float:
        return sum([item.size for item in self.content])

file_a = File('file_a', 12)
file_b = File('file_b', 32)
file_c = File('file_c', 45)

folder_a = Folder('folder_a', [file_a])
folder_b = Folder('folder_b', [folder_a, file_b, file_c])

size1 = folder_a.size
size2 = folder_b.size
print(f"{size1} == {12} {size1==12}")
print(f"{size2} == {89} {size2==89}")
assert size1 == folder_a.get_size()
assert size2 == folder_b.get_size()