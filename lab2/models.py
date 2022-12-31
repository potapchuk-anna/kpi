from uuid import uuid4
from typing import List 


class FileSystem:
    root = None
        
from typing import List

class Directory:
    def __init__(self, title, dir_max_elems, parent_folder):
        self.id = str(uuid4())
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
    def delete(self):
        self.parent_folder.subdirectoryList.remove(self)
    def list_of_subitems(self):
        subitems = []
        for item in self.subdirectoryList:
            subitems.append(item)
        for item in self.fileList:
            subitems.append(item)
        return subitems
    def move(self, path:str):
        folder = self
        nodes = path.split("/")
        for node in nodes:
            if node == "..":
                folder=folder.parent_folder
            elif node == ".":
                folder = folder
            else:
                contain = False
                for dir in folder.subdirectoryList:
                    if dir.title == node:
                        contain=True
                        folder=dir
                        break
                if contain==False:
                    raise FileNotFoundError("wrong path")
        self.parent_folder.subdirectoryList.remove(self)
        folder.subdirectoryList.append(self)
        self.parent_folder = folder


class BinaryFile:

    def __init__(self, title, content, parent_folder):
        self.id = str(uuid4())
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

    def delete(self):
        self.parent_folder.fileList.remove(self)
    def move(self, path:str):
        folder = self.parent_folder
        nodes = path.split("/")
        for node in nodes:
            if node == "..":
                folder=folder.parent_folder
            elif node == ".":
                folder = folder
            else:
                contain = False
                for dir in folder.subdirectoryList:
                    if dir.title == node:
                        contain=True
                        folder=dir
                        break
                if contain==False:
                    raise FileNotFoundError("wrong path")
        self.parent_folder.fileList.remove(self)
        folder.fileList.append(self)
        self.parent_folder = folder
    def read_file(self):
        return self.content

class LogTextFile:
    def __init__(self, title, content, parent_folder):
        self.id = str(uuid4())
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
    def delete(self):
        self.parent_folder.fileList.remove(self)
    def move(self, path:str):
        folder = self.parent_folder
        nodes = path.split("/")
        for node in nodes:
            if node == "..":
                folder=folder.parent_folder
            elif node == ".":
                folder = folder
            else:
                contain = False
                for dir in folder.subdirectoryList:
                    if dir.title == node:
                        contain=True
                        folder=dir
                        break
                if contain==False:
                    raise FileNotFoundError("wrong path")
        self.parent_folder.fileList.remove(self)
        folder.fileList.append(self)
        self.parent_folder = folder
    def read_file(self)->List[str]:
        return self.content
    def append_lines(self,lines:List[str]):
        for line in lines:
            self.content.append(line)

class BufferFile:
    def __init__(self, title, content, parent_folder, max_buf_file_size):
        self.id = str(uuid4())
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
    def delete(self):
        self.parent_folder.fileList.remove(self)
    def move(self, path:str):
        folder = self.parent_folder
        nodes = path.split("/")
        for node in nodes:
            if node == "..":
                folder=folder.parent_folder
            elif node == ".":
                folder = folder
            else:
                contain = False
                for dir in folder.subdirectoryList:
                    if dir.title == node:
                        contain=True
                        folder=dir
                        break
                if contain==False:
                    raise FileNotFoundError("wrong path")
        self.parent_folder.fileList.remove(self)
        folder.fileList.append(self)
        self.parent_folder = folder
    def push_element(self, line:str):
        if len(self.content)==self.max_buf_file_size:
            raise OverflowError("cannot append more than max lines")
        self.content.insert(0,line)
    def consume_element(self)->str:
        buff =  self.content[0]
        self.content.pop(0)
        return buff
