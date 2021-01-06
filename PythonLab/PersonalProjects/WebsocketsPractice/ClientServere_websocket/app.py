from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import request, render_template
import logging
import json

from utils.init_app import app, sockets, host, port, html_protocol, web_socket_protocol

from utils.sockets_manager import SocketsManager

logger = logging.getLogger(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    base_url = f"{host}:{port}" if 'HTTP_HOST' not in request.environ else request.environ['HTTP_HOST']
    data = {"html_protocol": html_protocol, "base_url": base_url}
    return render_template('sign.html', **data)


@app.route('/home', methods=['GET'])
def home():
    reqArgs = request.args.to_dict()
    base_url = f"{host}:{port}" if not 'HTTP_HOST' in request.environ else request.environ['HTTP_HOST']
    UserName = reqArgs.get("UserName", "No name")
    data = {"html_protocol": html_protocol,
            "base_url": base_url,
            "UserName": UserName,
            "UserId": "pending",
            "web_socket_protocol": web_socket_protocol
            }
    return render_template('home.html', **data)


@sockets.route('/socketHandler')
def socketHandler(socket):
    SocketsManager.login_protocol(socket)
    while not socket.closed:
        try:
            receive = socket.receive()
            if type(receive) == str:
                message = json.loads(receive)
                SocketsManager.send_message_to_all(socket, message)
        except Exception as e:
            logger.error(f"Error in socket: {socket} error message: {e}")
    if socket.closed:
        SocketsManager.disconnect_socket(socket)


if __name__ == '__main__':

    http_server = WSGIServer((host, port), app, log=logger, handler_class=WebSocketHandler)
    logger.info(f"Starting server at: {html_protocol}://{host}:{port}")
    http_server.serve_forever()
