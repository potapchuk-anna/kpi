import pytest
from lab2.models import Directory, BinaryFile, BufferFile, LogTextFile, FileSystem
from lab2.utils import request

def test_can_delete_directory():
    FileSystem.root = Directory("dir", 2, None)
    child_directory = Directory("dir2", 10, FileSystem.root)
    response = request(f'/directory/{child_directory.id}', method='DELETE')
    assert child_directory not in FileSystem.root.subdirectoryList
    assert response == (200, {})
    FileSystem.root = None


def test_can_move_directory():
    FileSystem.root = Directory("dir", 2, None)
    child_directory = Directory("dir1", 10, FileSystem.root)
    child_directory2 = Directory("dir2", 10, FileSystem.root)
    response = request(f'/directory/move/{child_directory.id}', method='PUT',
                       body={
                           "path": "../dir2"
                       })
    assert child_directory not in FileSystem.root.subdirectoryList and child_directory in child_directory2.subdirectoryList
    assert response == (200, {})
    FileSystem.root = None


def test_when_add_more_than_max_items_should_fail():
    FileSystem.root = Directory("dir", 2, None)
    child_directory1 = Directory("dir1", 10, FileSystem.root)
    response = request(f'/directory', method='POST', body={
        "title": "dir2",
        "dir_max_elems": 10,
        "parent_folder": FileSystem.root.id
    })
    assert response == (400, {})
    FileSystem.root = None


def test_when_create_directories_with_the_same_name_in_one_directory_fail():
    FileSystem.root = Directory("dir", 2, None)
    child_directory1 = Directory("dir1", 10, FileSystem.root)
    response = request(f'/directory', method='POST', body={
        "title": "dir1",
        "dir_max_elems": 10,
        "parent_folder": FileSystem.root.id
    })
    assert response == (400, {})
    FileSystem.root = None

def test_when_delete_folder_that_is_not_exist_fail():
    FileSystem.root = Directory("dir", 2, None)
    response = request(f'/directory/qweerererer', method='DELETE')
    assert response == (404, {})
    FileSystem.root = None

def test_can_delete_binary_file():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", FileSystem.root)
    response = request(f'/binaryfile/{file.id}', method='DELETE')
    assert file not in FileSystem.root.fileList
    assert response == (200, {})
    FileSystem.root = None

def test_when_delete_binary_file_that_is_not_exist_fail():
    FileSystem.root = Directory("dir", 2, None)
    response = request(f'/binaryfile/qweerererer', method='DELETE')
    assert response == (404, {})
    FileSystem.root = None

def test_can_move_binary_file():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", FileSystem.root)
    child_directory1 = Directory("dir1", 10, FileSystem.root)
    response = request(f'/binaryfile/move/{file.id}', method='PUT',
                       body={
                           "path": "./dir1"
                       })
    assert file in child_directory1.fileList and file not in FileSystem.root.fileList
    assert response == (200, {})
    FileSystem.root = None

def test_when_move_binary_file_that_is_not_exist_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", FileSystem.root)
    child_directory1 = Directory("dir1", 10, FileSystem.root)
    response = request(f'/binaryfile/move/trtyryrtyrty', method='PUT',
                       body={
                           "path": "./dir1"
                       })
    assert response == (404, {})
    FileSystem.root = None

def test_can_read_binary_file():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", FileSystem.root)
    response = request(f'/binaryfile/read/{file.id}', method='GET')
    assert response == (200, {
        "text": "some text"
    })
    FileSystem.root = None

def test_when_read_binary_file_that_is_not_exist_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", FileSystem.root)
    response = request(f'/binaryfile/read/ertertertet', method='GET')
    assert response == (404, {})
    FileSystem.root = None
def test_when_move_binary_file_with_wrong_path_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", FileSystem.root)
    response = request(f'/binaryfile/move/{file.id}', method='PUT',
                       body={
                           "path": "./dir1"
                       })
    assert response == (404, {})
    FileSystem.root = None

def test_when_move_binary_file_with_null_path_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", FileSystem.root)
    response = request(f'/binaryfile/move/{file.id}', method='PUT',
                       body={
                           "path": None
                       })
    assert response == (400, {})
    FileSystem.root = None
def test_when_create_binary_file_with_same_names_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", FileSystem.root)
    response = request(f'/binaryfile', method='POST', body={
        "title": "bin_file",
        "content": "some text",
        "parent_folder": FileSystem.root.id
    })
    assert response == (400, {})
    FileSystem.root = None
def test_when_create_binary_file_with_null_parent_id_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", FileSystem.root)
    response = request(f'/binaryfile', method='POST', body={
        "title": "bin_file",
        "content": "some text",
        "parent_folder": None
    })
    assert response == (400, {})
    FileSystem.root = None

def test_when_create_binary_file_with_null_parameters_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", FileSystem.root)
    response = request(f'/binaryfile', method='POST')
    assert response == (400, {})
    FileSystem.root = None

def test_when_create_binary_file_with_null_title_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("bin_file", "some text", FileSystem.root)
    response = request(f'/binaryfile', method='POST', body={
        "title": None,
        "content": "some text",
        "parent_folder": FileSystem.root.id
    })
    assert response == (400, {})
    FileSystem.root = None
def test_can_delete_log_file():
    FileSystem.root = Directory("dir", 2, None)
    file = LogTextFile("log_file", "some text", FileSystem.root)
    response = request(f'/logtextfile/{file.id}', method='DELETE')
    assert file not in FileSystem.root.fileList
    assert response == (200, {})
    FileSystem.root = None


def test_can_move_log_file():
    FileSystem.root = Directory("dir", 2, None)
    file = LogTextFile("log_file", "some text", FileSystem.root)
    child_directory1 = Directory("dir1", 10, FileSystem.root)
    response = request(f'/logtextfile/move/{file.id}', method='PUT',
                       body={
                           "path": "./dir1"
                       })
    assert file in child_directory1.fileList and file not in FileSystem.root.fileList
    assert response == (200, {})
    FileSystem.root = None


def test_can_read_log_file():
    FileSystem.root = Directory("dir", 2, None)
    file = LogTextFile("log_file", ["some text", "some text 2"], FileSystem.root)
    response = request(f'/logtextfile/read/{file.id}', method='GET')
    assert response == (200, {
        "text": ["some text", "some text 2"]
    })
    FileSystem.root = None


def test_can_append_lines_in_log_file():
    FileSystem.root = Directory("dir", 2, None)
    file = LogTextFile("log_file", ["some text", "some text 2"], FileSystem.root)
    response = request(f'/logtextfile/{file.id}/append', method='PUT', body={
        "lines": ["last line"]
    })
    assert response == (200, {})
    assert file.content == ["some text", "some text 2", "last line"]
    FileSystem.root = None


def test_when_move_log_file_with_wrong_path_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("log_file", "some text", FileSystem.root)
    response = request(f'/logtextfile/move/{file.id}', method='PUT',
                       body={
                           "path": "./dir1"
                       })
    assert response == (400, {})
    FileSystem.root = None


def test_when_create_log_file_with_same_names_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("log_file", "some text", FileSystem.root)
    response = request(f'/logtextfile', method='POST', body={
        "title": "log_file",
        "content": "some text",
        "parent_folder": FileSystem.root.id
    })
    assert response == (400, {})
    FileSystem.root = None


def test_can_delete_buff_file():
    FileSystem.root = Directory("dir", 2, None)
    file = LogTextFile("buff_file", "some text", FileSystem.root)
    response = request(f'/bufferfile/{file.id}', method='DELETE')
    assert file not in FileSystem.root.fileList
    assert response == (200, {})
    FileSystem.root = None


def test_can_move_buff_file():
    FileSystem.root = Directory("dir", 2, None)
    file = LogTextFile("buff_file", "some text", FileSystem.root)
    child_directory1 = Directory("dir1", 10, FileSystem.root)
    response = request(f'/bufferfile/move/{file.id}', method='PUT',
                       body={
                           "path": "./dir1"
                       })
    assert file in child_directory1.fileList and file not in FileSystem.root.fileList
    assert response == (200, {})
    FileSystem.root = None


def test_when_move_buff_file_with_wrong_path_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("buff_file", "some text", FileSystem.root)
    response = request(f'/bufferfile/move/{file.id}', method='PUT',
                       body={
                           "path": "./dir1"
                       })
    assert response == (400, {})
    FileSystem.root = None


def test_can_push_lines_in_buff_file():
    FileSystem.root = Directory("dir", 2, None)
    file = BufferFile("buff_file", ["some text", "some text 2"], FileSystem.root, 4)
    response = request(f'/bufferfile/{file.id}/push', method='PUT',
                       body={
                           "lines": "first line"
                       })
    assert response == (200, {})
    assert file.content == ["first line", "some text", "some text 2"]
    FileSystem.root = None


def test_can_consume_line_in_buff_file():
    FileSystem.root = Directory("dir", 2, None)
    file = BufferFile("buff_file", ["some text", "some text 2"], FileSystem.root, 4)
    response = request(f'/bufferfile/{file.id}/consume', method='PUT')
    assert file.content == ["some text 2"]
    assert response == (200, {
        "text": "some text"
    })
    FileSystem.root = None


def test_when_create_buff_file_with_same_names_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BinaryFile("buff_file", "some text", FileSystem.root)
    response = request(f'/bufferfile', method='POST', body={
        "title": "buff_file",
        "content": "some text",
        "parent_folder": FileSystem.root.id
    })
    assert response == (400, {})
    FileSystem.root = None


def test_when_push_more_than_max_fail():
    FileSystem.root = Directory("dir", 2, None)
    file = BufferFile("buff_file", ["some text", "some text 2"], FileSystem.root, 2)
    response = request(f'/bufferfile/{file.id}/push', method='PUT',
                       body={
                           "content": "first line"
                       })
    assert file.content == ["some text", "some text 2"]
    assert response == (400, {})
    FileSystem.root = None
