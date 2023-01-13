import sys
from utils import request

def main(args):
    response = parser(args)
    print(f"{response[0]};{response[1]}")


def parser(args):
    if len(args) < 1:
        print("Such command does not exist.")
    else:
        entity = args[0]
        if entity not in ['binaryfile', 'logtextfile', 'bufferfile', 'directory']:
            print("Such command does not exist.")
            return
        operation = args[1]
        if operation == "get_root" and entity == 'directory':
            if validate_min_length(args, 2) == False:
                return {
                    "exception": "Not all parameters were writen"
                }, 400
            path = f'{entity}/root'
            return request(path)
        if operation == "create":
            if validate_min_length(args, 5) == False:
                return {
                    "exception": "Not all parameters were writen"
                }, 400
            if entity in ['binaryfile', 'logtextfile', 'bufferfile']:
                if args[3].lower() == "none" or args[3].lower() == "null":
                    body = {
                        "title": args[2],
                        "content": None,
                        "parent_folder": args[4]
                    }
                else:
                    if entity in ['binaryfile', 'logtextfile']:
                        content = " ".join(args[3:len(args)-1])
                    else:
                        content = args[3:len(args) - 1]
                    body = {
                        "title": args[2],
                        "content": content,
                        "parent_folder": args[len(args)-1]
                    }
                path = f"/{entity}"
                return request(path, method='POST', body=body)
            elif entity == 'directory':
                parent_folder = args[4]
                if parent_folder.lower() == "none" or parent_folder.lower() == "null":
                    body = {
                        "title": args[2],
                        "dir_max_elements": int(args[3]),
                        "parent_folder": None
                    }
                else:
                    body = {
                        "title": args[2],
                        "dir_max_elements": args[3],
                        "parent_folder": args[4]
                    }
                path = f"/{entity}"
                return request(path, method='POST', body=body)
        if operation == "delete":
            if validate_min_length(args, 3) == False:
                return {
                    "exception": "Not all parameters were writen"
                }, 400
            uuid = args[2]
            path = f"/{entity}/{uuid}"
            return request(path, method='DELETE')
        if operation == 'move':
            if validate_min_length(args, 4) == False:
                return {
                    "exception": "Not all parameters were writen"
                }, 400
            uuid = args[2]
            body = {
                "path": args[3]
            }
            path = f"/{entity}/{operation}/{uuid}"
            return request(path, method='PUT', body=body)
        if operation == 'get-items' and entity == 'directory':
            if validate_min_length(args, 3) == False:
                return {
                    "exception": "Not all parameters were writen"
                }, 400
            uuid = args[2]
            path = f"/{entity}/{uuid}/items"
            return request(path)
        if operation == 'read' and entity in ["binaryfile", "logtextfile", "bufferfile"]:
            if validate_min_length(args, 3) == False:
                return {
                    "exception": "Not all parameters were writen"
                }, 400
            uuid = args[2]
            path = f"/{entity}/{operation}/{uuid}"
            return request(path)
        if operation == 'append':
            if validate_min_length(args, 4) == False:
                return {
                    "exception": "Not all parameters were writen"
                }, 400
            uuid = args[2]
            body = {
                "lines": args[3:]
            }
            path = f"/{entity}/{uuid}/{operation}"
            return request(path, method='PUT', body=body)
        if operation == 'push' and entity == 'bufferfile':
            if validate_min_length(args, 4) == False:
                return {
                    "exception": "Not all parameters were writen"
                }, 400
            uuid = args[2]
            body = {
                "line": args[3]
            }
            path = f"/{entity}/{uuid}/{operation}"
            return request(path, method='PUT', body=body)
        if operation == 'consume' and entity == 'bufferfile':
            if validate_min_length(args, 3) == False:
                return {
                    "exception": "Not all parameters were writen"
                }, 400
            uuid = args[2]
            path = f"/{entity}/{uuid}/{operation}"
            return request(path, method='PUT')




def validate_min_length(args, number):
    if len(args) >= number:
        return True
    else:
        return False

if __name__ == "__main__":
    main(sys.argv[1:])
