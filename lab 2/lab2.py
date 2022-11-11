from flask import Flask
from flask import request
import json
from uuid import UUID
from models import Directory, BinaryFile, BufferFile, LogTextFile, FileSystem

app = Flask(__name__)



@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name

@app.route('/he')
def hello():
    name = request.get_json("name")
    return 'Hello %s!' % name

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
   
    
    # Serializing json
    json_object = json.dumps(Directory("root", 1000, None).__dict__, cls=UUIDEncoder, indent=4)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
   
    app.run()


