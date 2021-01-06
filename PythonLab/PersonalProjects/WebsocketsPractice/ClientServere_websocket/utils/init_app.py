import os
import argparse
from flask import Flask
from flask_sockets import Sockets
import logging

root_path = os.getcwd()
template_folder = os.path.join(root_path, 'templates')
static_folder = os.path.join(root_path, 'static')
log_path = os.path.join(root_path, 'logs', 'log.txt')

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s   %(levelname)s   %(message)s', filename='logs/log.txt')
logging.getLogger().addHandler(logging.StreamHandler())
# logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
sockets = Sockets(app)
# global UsersSockets, UsersDict

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--port', '-p', type=int, help='port to lissen server on', default=5443)
parser.add_argument('--host', help='host to connect server to', default='0.0.0.0')
parser.add_argument('--html_protocol', default='http')
parser.add_argument('--web_socket_protocol', default='ws')
args = parser.parse_args()

# Configurations:
debug_mode = True
port = args.port  # SSL default port
host = args.host  # localhost default
html_protocol = args.html_protocol
web_socket_protocol = args.web_socket_protocol

app.debug = debug_mode
