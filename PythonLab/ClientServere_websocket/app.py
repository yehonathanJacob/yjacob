from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import argparse
from flask import Flask, request,render_template
from flask_sockets import Sockets
import logging
import json

logging.basicConfig(level=logging.INFO, format= '%(asctime)-15s   %(levelname)s   %(message)s')

app = Flask(__name__)
sockets = Sockets(app)
global UsersSockets, UsersDict

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

@app.route('/', methods=['POST', 'GET'])
def index():
    base_url = f"{host}:{port}" if not 'HTTP_HOTS' in request.environ else request.environ['HTTP_HOTS']
    data = {"html_protocol": html_protocol,"base_url":base_url}
    return render_template('sign.html',**data)

@app.route('/home', methods=['GET'])
def home():
    reqArgs = request.args.to_dict()
    base_url = f"{host}:{port}" if not 'HTTP_HOTS' in request.environ else request.environ['HTTP_HOTS']
    UserName = reqArgs.get("UserName","No name")
    data = {"html_protocol": html_protocol,
            "base_url":base_url,
            "UserName": UserName,
            "UserId": "pending",
            "web_socket_protocol":web_socket_protocol
            }
    return render_template('home.html',**data)

@sockets.route('/socketHandler')
def socketHandler(socket):
    loginProtocol(socket)
    while not socket.closed:
        try:
            receive = socket.receive()
            if type(receive) == str:
                message = json.loads(receive)
                sendMessageToAll(socket,message)
        except Exception as e:
            logging.error(f"Error in socket: {socket} error message: {e}")
    if socket.closed:
        disconnectSocket(socket)

def disconnectSocket(DeleteSocket):
    User = UsersDict[DeleteSocket]
    logging.info(f"Disconnect socket: name: {User['name']}\tID: {User['ID']}")
    del UsersDict[DeleteSocket]
    UsersSockets.remove(DeleteSocket)
    sendNotification(User['name'], 'sign_out')

def loginProtocol(socket):
    OpennnigData = json.loads(socket.receive())
    name = OpennnigData['name']
    ID = socket.environ['REMOTE_PORT']
    socket.send(json.dumps({'status': 'NewID', "ID": ID}))
    UsersSockets.add(socket)
    UsersDict[socket] = {'name':name,'ID':ID}
    logging.info(f"New socket: name: {name}\tID: {ID}")
    sendNotification(name,'sign_in')

def sendMessageToAll(SenderSocket,message):
    Sender = UsersDict[SenderSocket]
    SenderMessage = message['content']
    SenderID = Sender['ID']
    SenderName = Sender['name']
    logging.info(f"Sending from: {SenderName}\t message: {SenderMessage}")
    jsonData = {'status':'Message','UserId':SenderID,'UserName':SenderName,'Content':SenderMessage.replace("\n","<br>")}
    outputToSockets(jsonData)

def sendNotification(UserName,StatusMessage):
    jsonData = {'status':'Login','UserName':UserName,'StatusMessage':StatusMessage}
    outputToSockets(jsonData)

def outputToSockets(jsonData):
    for socket in UsersSockets:
        socket.send(json.dumps(jsonData))

if __name__ == '__main__':
    UsersSockets = set()
    UsersDict = {}
    app.debug = debug_mode
    http_server = WSGIServer((host,port),app,log=logging, handler_class=WebSocketHandler)
    logging.info(f"Starting server at: {html_protocol}://{host}:{port}")
    http_server.serve_forever()
