from uuid import uuid4
from typing import List 


class FileSystem:
    def __init__(self, root):
        self.root = root
        
class Directory:
    def __init__(self, title, dir_max_elems, parent_folder):
        self.id = uuid4()
        self.fileList = []
        self.subdirectoryList = []
        self.dir_max_elems = dir_max_elems
        self.title= title
        self.parent_folder = parent_folder
        if parent_folder is not None:
            if self.parent_folder.dir_max_elems==len(self.parent_folder.list_of_subitems()):
                raise OverflowError("elements in directory more than max")
            for dir in self.parent_folder.subdirectoryList:
                if dir.title == self.title:
                    raise ValueError("cannot add two files with same name")
            self.parent_folder.subdirectoryList.append(self)

class BinaryFile:
    def __init__(self, title, content, parent_folder):
        self.id = uuid4()
        self.title = title
        self.content = content
        self.parent_folder = parent_folder
        if parent_folder is not None:
            if self.parent_folder.dir_max_elems==len(self.parent_folder.list_of_subitems()):
                raise OverflowError("elements in directory more than max")
            for file in self.parent_folder.fileList:
                if file.title == self.title:
                    raise FileExistsError("cannot add two files with same name")
            self.parent_folder.fileList.append(self)

class LogTextFile:
    def __init__(self, title, content, parent_folder):
        self.id = uuid4()
        self.title = title
        self.content: List[str] = content
        self.parent_folder = parent_folder
        if parent_folder is not None:
            if self.parent_folder.dir_max_elems==len(self.parent_folder.list_of_subitems()):
                raise OverflowError("elements in directory more than max")
            for file in self.parent_folder.fileList:
                if file.title == self.title:
                    raise FileExistsError("cannot add two files with same name")
            self.parent_folder.fileList.append(self)

class BufferFile:
    def __init__(self, title, content, parent_folder, max_buf_file_size):
        self.id = uuid4()
        self.title = title
        self.content:List[str] = content
        self.parent_folder = parent_folder
        self.max_buf_file_size = max_buf_file_size
        if parent_folder is not None:
            if self.parent_folder.dir_max_elems==len(self.parent_folder.list_of_subitems()):
                raise OverflowError("elements in directory more than max")
            for file in self.parent_folder.fileList:
                if file.title == self.title:
                    raise FileExistsError("cannot add two files with same name")
            self.parent_folder.fileList.append(self)

