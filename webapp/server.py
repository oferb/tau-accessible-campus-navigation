import wakkaide.network_file
wakkaide.network_file.setup()
from flask import Flask
from flask import request
import requests
import time
import threading
import os

# This is an example of a basic Flask server.
# Feel free to try it for yourself!

app = Flask(__name__)

@app.route("/")
def index():
  f = open('tau_smartcities/webapp/public/html/navigation_page4.html', "r")
  return f.read(), 200, {'Content-Type': 'text/html'}

@app.route("/<path:path>", methods = ['GET'])
def get_file(path):
  try:
    f = open('tau_smartcities/webapp/public/' + path, "rb" if is_binary(path) else "r")
    return f.read(), 200, {'Content-Type': get_content_type(path)}
  except FileNotFoundError:
    error_message = 'FileNotFoundError: No such file: ' + path
    print(error_message)
    return error_message, 404, {'Content-Type': 'text/html'} 

@app.route('/<path:path>', methods = ['POST'])
def post(path):
  print(request)
  print(request.form)

@app.route("/roads/<roadName>")
def get_road(roadName):
  """(BAR) this function is here for encapsulating json file requests 
     jsons are now accessible through roads/<name_of_json>
   """
  file_path = "tau_smartcities/webapp/public/assets/jsons/" + roadName 
  try:
    with open(file_path, "r", "utf-8" ) as road_file:
      return road_file.read(), 200, {'Content-Type': 'text/html'}

  except FileNotFoundError:
    error_message = 'FileNotFoundError: No such file: roads/{0} '.format(roadName)
    print(error_message)
    return error_message, 404, {'Content-Type': 'text/html'} 

def get_content_type(path):
  print(path)
  if path.endswith('.html'):
    return 'text/html'
  if path.endswith('.json'):
    return 'application/json'
  if path.endswith('.js'):
    return 'text/javascript'
  if path.endswith('.txt'):
    return 'text/plain'
  if path.endswith('.css'):
    return 'text/css'
  if path.endswith('.svg'):
    return 'image/svg+xml'
  if path.endswith('.ico'):
    return 'image/x-icon'
  if path.endswith('.png'):
    return 'image/png'
  if path.endswith('.jpg'):
    return 'image/jpeg'
  if path.endswith('.gif'):
    return 'image/gif'

def is_binary(path):
  _, file_extension = os.path.splitext(path)
  return file_extension in ['.ico', '.png', '.jpg', '.gif']

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
