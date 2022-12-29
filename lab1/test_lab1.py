import pytest
from lab1.lab1 import Directory, BinaryFile, BufferFile, LogTextFile


def test_can_delete_directory():
    directory =  Directory("dir", 2, None)
    child_directory = Directory("dir2", 10, directory)
    child_directory.delete()
    assert child_directory not in directory.subdirectoryList 

def test_can_move_directory():
    directory =  Directory("dir", 2, None)
    child_directory = Directory("dir1", 10, directory)
    child_directory2 = Directory("dir2", 10, directory)
    path="../dir2"
    child_directory.move(path)
    assert child_directory not in directory.subdirectoryList and child_directory in child_directory2.subdirectoryList

def test_when_add_more_than_max_items_should_fail():
    directory =  Directory("dir", 2, None)
    child_directory1 = Directory("dir1", 10, directory)
    child_directory2 = Directory("dir2", 10, directory)
    with pytest.raises(OverflowError):
        child_directory3 = Directory("dir3", 10, directory)

def test_when_create_directories_with_the_same_name_in_one_directory_fail():
    directory =  Directory("dir", 2, None)
    child_directory1 = Directory("dir1", 10, directory)
    with pytest.raises(ValueError):
        child_directory2 = Directory("dir1", 10, directory)


def test_can_delete_binary_file():
    directory =  Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", directory)
    file.delete()
    assert file not in directory.fileList
    
def test_can_move_binary_file():
    directory =  Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", directory)
    child_directory1 = Directory("dir1", 10, directory)
    file.move("./dir1")
    assert file in child_directory1.fileList and file not in directory.fileList

def test_can_read_binary_file():
    directory =  Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", directory)
    assert file.read_file() == "some text"

def test_when_move_binary_file_with_wrong_path_fail():
    directory =  Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", directory)
    with pytest.raises(FileNotFoundError):
        file.move("./dir1")

def test_when_create_binary_file_with_same_names_fail():
    directory =  Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", directory)
    with pytest.raises(FileExistsError):
        file1 = BinaryFile("bin_file", "some text", directory)


def test_can_delete_log_file():
    directory =  Directory("dir", 2, None)
    file = LogTextFile("log_file", "some text", directory)
    file.delete()
    assert file not in directory.fileList
    
def test_can_move_log_file():
    directory =  Directory("dir", 2, None)
    file = LogTextFile("log_file", "some text", directory)
    child_directory1 = Directory("dir1", 10, directory)
    file.move("./dir1")
    assert file in child_directory1.fileList and file not in directory.fileList

def test_can_read_log_file():
    directory =  Directory("dir", 2, None)
    file = LogTextFile("log_file", ["some text", "some text 2"], directory)
    assert file.read_file()==["some text", "some text 2"]

def test_can_append_lines_in_log_file():
    directory =  Directory("dir", 2, None)
    file = LogTextFile("log_file", ["some text", "some text 2"], directory)
    file.append_lines(["last line"])
    assert file.read_file()==["some text", "some text 2","last line"]

def test_when_move_log_file_with_wrong_path_fail():
    directory =  Directory("dir", 2, None)
    file = LogTextFile("log_file", "some text", directory)
    with pytest.raises(FileNotFoundError):
        file.move("./dir1")

def test_when_create_log_file_with_same_names_fail():
    directory =  Directory("dir", 2, None)
    file = LogTextFile("log_file", "some text", directory)
    with pytest.raises(FileExistsError):
        file1 = LogTextFile("log_file", "some text", directory)



def test_can_delete_buff_file():
    directory =  Directory("dir", 2, None)
    file = BufferFile("buff_file", ["some text"], directory, 4)
    file.delete()
    assert file not in directory.fileList
    
def test_can_move_buff_file():
    directory =  Directory("dir", 2, None)
    file = BufferFile("buff_file", ["some text"], directory, 4)
    child_directory1 = Directory("dir1", 10, directory)
    file.move("./dir1")
    assert file in child_directory1.fileList and file not in directory.fileList

def test_when_move_buff_file_with_wrong_path_fail():
    directory =  Directory("dir", 2, None)
    file = BufferFile("buff_file", ["some text"], directory, 4)
    with pytest.raises(FileNotFoundError):
        file.move("./dir1")

def test_can_push_lines_in_buff_file():
    directory =  Directory("dir", 2, None)
    file = BufferFile("buff_file", ["some text", "some text 2"], directory, 4)
    file.push_element("first line")
    assert file.content == ["first line", "some text", "some text 2"]

def test_can_consume_line_in_buff_file():
    directory =  Directory("dir", 2, None)
    file = BufferFile("buff_file", ["some text", "some text 2"], directory, 4)   
    assert file.consume_element()=="some text" and file.content == ["some text 2"]

def test_when_create_buff_file_with_same_names_fail():
    directory =  Directory("dir", 2, None)
    file = BufferFile("buff_file", ["some text"], directory, 4)
    with pytest.raises(FileExistsError):
        file1 = BufferFile("buff_file", ["some text"], directory, 4)
def test_when_push_more_than_max_fail():
    directory =  Directory("dir", 2, None)
    file = BufferFile("buff_file", ["some text", "some text 2"], directory, 2)
    with pytest.raises(OverflowError):
        file.push_element("first line")
