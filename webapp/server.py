import wakkaide.network_file
wakkaide.network_file.setup()
from flask import Flask
import os
import mimetypes
import json
mimetypes.init()

app = Flask(__name__)
jsons_response = None

@app.route('/', defaults={'path': ''})
@app.route("/<path:path>")
def get_file(path):
  path = get_path_in_public(path)
  mode = "rb" if is_binary(path) else "r"

  try:
    with open(path, mode) as f: 
      return f.read(), 200, {'Content-Type': get_mime(path)}

  except FileNotFoundError:
    error_message = 'FileNotFoundError: No such file: ' + path
    print(error_message)
    return error_message, 404, {'Content-Type': 'text/html'}

@app.route('/<path:path>', methods = ['POST'])
def post(path):
  print(request)
  print(request.form)

@app.route('/jsons')
def jsons():
  global jsons_response
  if not jsons_response:
    all_jsons = []
    for i in range(5):
      path = get_path_in_public("jsons/{0}.json".format(i))
      with open(path, "r",) as current_json_file:
        all_jsons.append(json.load(current_json_file))
    jsons_response = json.dumps(all_jsons, ensure_ascii=False), 200, {'Content-Type': get_mime(path)}
  return jsons_response

def get_path_in_public(path:str):
  if not path:
    path = os.path.join(path, 'app.html')
  
  relative_path = os.path.relpath(os.path.dirname(__file__), '/code/root')
  return os.path.join(relative_path, 'public', path)

def get_mime(path):
  extension = os.path.splitext(path)[-1]
  return mimetypes.types_map[extension]

def is_binary(path):
  _, file_extension = os.path.splitext(path)
  return file_extension in ['.ico', '.png', '.jpg', '.gif']


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)


