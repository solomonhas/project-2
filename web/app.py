"""
John Doe's Flask API.
"""
import os
import configparser

from flask import Flask, send_from_directory

app = Flask(__name__, template_folder = 'pages')

# Read configuration file
config = configparser.ConfigParser()
config_file = 'credentials.ini'
if not os.path.exists(config_file):
    config_file = 'default.ini'
config.read(config_file)

#Getmport number and debug mode from credentials.ini
port = int(config['SERVER']['PORT'])
debug = config['SERVER']['DEBUG'].lower() == 'true' 

def send_error(error_code):
    error_file = None
    if error_code == 404:
        error_file = '404.html' #display the 404 file if not found
    elif error_code == 403:
        error_file = '403.html' #display the 403 file if forbidden chars
    else:
        return "", error_code

    pages_dir = os.path.join(app.root_path, 'pages')
    file_path = os.path.join(pages_dir, error_file)
    return send_from_directory(pages_dir, error_file), error_code

@app.route("/")
def hello():
    return "UOCIS docker demo!\n"

@app.route('/<path:path>')
def serve_file(path):
    if ".." in path or "~" in path:
        return send_error(403)

    pages_dir = os.path.join(app.root_path, 'pages')
    file_path = os.path.join(pages_dir, path)
    if os.path.isfile(file_path):
        return send_from_directory(pages_dir, path)
    else:
        return send_error(404)

if __name__ == "__main__":
    app.run(debug=debug, host='0.0.0.0', port=port)

