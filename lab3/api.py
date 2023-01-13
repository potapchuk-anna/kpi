import json

from flask import Flask, request
from models import Directory, BinaryFile, BufferFile, LogTextFile, FileSystem

app = Flask(__name__)


@app.route('/directory', methods=['POST'])
def directory_create():
    request_body = json.loads(request.get_json())
    if request_body is None:
        return {
            "exception": "Request body is empty"
        }, 400
    if FileSystem.root is None and request_body['parent_folder'] is None:
        FileSystem.root = Directory(request_body['title'], request_body['dir_max_elements'], None)
        return {
            "root": FileSystem.root.id
        }, 200
    if FileSystem.root is not None and request_body['parent_folder'] is None:
        return {
            "exception": "Root folder already exist"
        }, 400
    if request_body['title'] is None:
        return {
            "exception": "Title should not be null"
        }, 400
    parent_folder = get_element_by_id(FileSystem.root, request_body['parent_folder'])
    if parent_folder is None:
        return {
            "exception": "You should mention parent folder"
        }, 404
    try:
        dir = Directory(request_body['title'], request_body['dir_max_elements'], parent_folder)
    except Exception as e:
        return {
            "exception": e.args[0]
        }, 400

    return {
        "dir_id": dir.id
    }, 200


@app.route('/directory/<id>', methods=['DELETE'])
def directory_delete(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    folder = get_element_by_id(FileSystem.root, id)
    if folder is None:
        return {
            "exception": "No such directory"
        }, 404
    folder.delete()
    return {}, 200


@app.route('/directory/<id>/items', methods=['GET'])
def get_folder_list(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    folder = get_element_by_id(FileSystem.root, id)
    if folder is None:
        return {
            "exception": "No such directory"
        }, 404
    items = folder.list_of_subitems()
    return {
        "id": folder.id,
        "title": folder.title,
        "items": items
    }, 200


@app.route('/directory/move/<id>', methods=['PUT'])
def directory_move(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    request_body = json.loads(request.get_json())
    folder = get_element_by_id(FileSystem.root, id)
    if folder is None:
        return {
            "exception": "No such directory"
        }, 404
    try:
        folder.move(request_body['path'])
    except Exception as e:
        return {
            "exception": e.args[0]
        }, 404
    return {}, 200

@app.route('/directory/root')
def get_root():
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    return {
        "root_id": FileSystem.root.id
    }, 200

@app.route('/directory/root', methods=['DELETE'])
def delete_root():
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    FileSystem.root.delete()
    return {}, 200

@app.route('/binaryfile', methods=['POST'])
def binfile_create():
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    request_body = json.loads(request.get_json())
    if request_body is None:
        return {
            "exception": "Request body should not be null"
        }, 400
    if request_body['parent_folder'] is None:
        return {
            "exception": "Parent folder should not be null"
        }, 400
    if request_body['title'] is None:
        return {
            "exception": "Title should not be null"
        }, 400
    parent_folder = get_element_by_id(FileSystem.root, request_body['parent_folder'])
    if parent_folder is None:
        return {
            "exception": "No such directory"
        }, 404
    try:
        file = BinaryFile(request_body['title'], request_body['content'], parent_folder)
    except Exception as e:
        return {
            "exception": e.args[0]
        }, 400
    return {"file_id": file.id}, 200


@app.route('/binaryfile/<id>', methods=['DELETE'])
def binfile_delete(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    file = get_element_by_id(FileSystem.root, id)
    if file is None:
        return {
            "exception": "No such file"
        }, 404
    file.delete()
    return {}, 200


@app.route('/binaryfile/read/<id>', methods=['GET'])
def binfile_read(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    file = get_element_by_id(FileSystem.root, id)
    if file is None:
        return {
            "exception": "No such file"
        }, 404
    return {
        "text": file.read_file()
    }, 200


@app.route('/binaryfile/move/<id>', methods=['PUT'])
def binfile_move(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    request_body = json.loads(request.get_json())
    file = get_element_by_id(FileSystem.root, id)
    if file is None:
        return {
            "exception": "No such file"
        }, 404
    path = request_body['path']
    if path is None:
        return {
            "exception": "Path should not be null"
        }, 400
    try:
        file.move(request_body['path'])
    except Exception as e:
        return {
            "exception": e.args[0]
        }, 400
    return {}, 200


@app.route('/logtextfile', methods=['POST'])
def logfile_create():
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    request_body = json.loads(request.get_json())
    if request_body is None:
        return {
            "exception": "Request body should not be null"
        }, 400
    if request_body['parent_folder'] is None:
        return {
            "exception": "Parent folder should not be null"
        }, 400
    if request_body['title'] is None:
        return {
            "exception": "Title should not be null"
        }, 400
    parent_folder = get_element_by_id(FileSystem.root, request_body['parent_folder'])
    if parent_folder is None:
        return {
            "exception": "No such directory"
        }, 404
    try:
        file = LogTextFile(request_body['title'], request_body['content'], parent_folder)
    except Exception as e:
        return {
            "exception": e.args[0]
        }, 400
    return {"file_id": file.id}, 200


@app.route('/logtextfile/<id>', methods=['DELETE'])
def logfile_delete(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    file = get_element_by_id(FileSystem.root, id)
    if file is None:
        return {
            "exception": "No such file"
        }, 404
    file.delete()
    return {}, 200


@app.route('/logtextfile/read/<id>', methods=['GET'])
def logfile_read(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    file = get_element_by_id(FileSystem.root, id)
    if file is None:
        return {
            "exception": "No such file"
        }, 404
    return {
        "text": file.read_file()
    }, 200


@app.route('/logtextfile/move/<id>', methods=['PUT'])
def logfile_move(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    request_body = json.loads(request.get_json())
    file = get_element_by_id(FileSystem.root, id)
    if file is None:
        return {
            "exception": "No such file"
        }, 404
    try:
        file.move(request_body['path'])
    except Exception as e:
        return {
            "exception": e.args[0]
        }, 400
    return {}, 200


@app.route('/logtextfile/<id>/append', methods=['PUT'])
def append(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    request_body = json.loads(request.get_json())
    file = get_element_by_id(FileSystem.root, id)
    if file is None:
        return {
            "exception": "No such file"
        }, 404
    file.append_lines(request_body['lines'])
    return {}, 200


@app.route('/bufferfile', methods=['POST'])
def bufffile_create():
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    request_body = json.loads(request.get_json())
    if request_body is None:
        return {
            "exception": "Request body should not be null"
        }, 400
    if request_body['parent_folder'] is None:
        return {
            "exception": "Parent folder should not be null"
        }, 400
    if request_body['title'] is None:
        return {
            "exception": "Title should not be null"
        }, 400
    parent_folder = get_element_by_id(FileSystem.root, request_body['parent_folder'])
    if parent_folder is None:
        return {
            "exception": "No such directory"
        }, 404
    try:
        file = BufferFile(request_body['title'], request_body['content'], parent_folder)
    except Exception as e:
        return {
            "exception": e.args[0]
        }, 400
    return {"file_id": file.id}, 200


@app.route('/bufferfile/<id>', methods=['DELETE'])
def bufffile_delete(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    file = get_element_by_id(FileSystem.root, id)
    if file is None:
        return {
            "exception": "No such file"
        }, 404
    file.delete()
    return {}, 200


@app.route('/bufferfile/read/<id>', methods=['GET'])
def bufffile_read(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    file = get_element_by_id(FileSystem.root, id)
    if file is None:
        return {
            "exception": "No such file"
        }, 404
    return json.dumps(file.read_file()), 200


@app.route('/bufferfile/move/<id>', methods=['PUT'])
def bufffile_move(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    request_body = json.loads(request.get_json())
    file = get_element_by_id(FileSystem.root, id)
    if file is None:
        return {
            "exception": "No such file"
        }, 404
    try:
        file.move(request_body['path'])
    except Exception as e:
        return {
            "exception": e.args[0]
        }, 400
    return {}, 200


@app.route('/bufferfile/<id>/push', methods=['PUT'])
def push(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    request_body = json.loads(request.get_json())
    if request_body is None:
        return {}, 400
    file = get_element_by_id(FileSystem.root, id)
    if file is None:
        return {
            "exception": "No such file"
        }, 404
    try:
        file.push_element(request_body['line'])
    except Exception as e:
        return {
            "exception": e.args[0]
        }, 400
    return {}, 200


@app.route('/bufferfile/<id>/consume', methods=['PUT'])
def consume(id):
    if FileSystem.root is None:
        return {
            "exception": "You should create root folder first"
        }, 400
    file = get_element_by_id(FileSystem.root, id)
    if file is None:
        return {
            "exception": "No such file"
        }, 404
    buff = file.consume_element()
    return {
        "text": buff
    }, 200


def get_element_by_id(source, id):
    if source is None:
        return None
    if source.id == id:
        return source
    if hasattr(source, "fileList"):

        for elem in source.fileList:
            if elem.id == id:
                return elem

        for elem in source.subdirectoryList:
            found = get_element_by_id(elem, id)
            if found is not None:
                return found
    return None


if __name__ == '__main__':
    app.run()
