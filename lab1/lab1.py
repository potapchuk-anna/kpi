from typing import List 

class Directory:
    def init(self, title, dir_max_elems:int, path):
        self.fileList = List()
        self.subdirectoryList = List()
        self.dir_max_element = dir_max_elems
        self.title= title
        self.path=path
    def delete(self):
        pass
    def list_of_subitems(self)->List[str]:
        pass
    def move(self, path:str):
        pass

class BinaryFile:

    def init(self, title, content, path):
        self.title = title
        self.content = content
        self.path = path

    def delete(self):
        pass
    def move(self, path:str):
        pass
    def read_file(self)->List[str]:
        pass

class LogTextFile:
    def init(self, title, content, path):
        self.title = title
        self.content = content
        self.path = path
    def delete(self):
        pass
    def move(self, path:str):
        pass
    def read_file(self)->List[str]:
        pass
    def append_lines(self,lines:List[str]):
        pass

class BufferFile:
    def init(self, title, content, path, max_buf_file_size):
        self.title = title
        self.content = content
        self.path = path
        self.max_buf_file_size = max_buf_file_size
    def delete(self):
        pass
    def move(self, path:str):
        pass
    def push_element(self, line:str):
        pass
    def consume_element(self)->str:
        pass