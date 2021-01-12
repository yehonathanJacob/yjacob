import logging
import json

logger = logging.getLogger(__name__)


class SocketsManager:
    UsersSockets = set()
    UsersDict = {}

    @classmethod
    def disconnect_socket(cls, DeleteSocket):
        User = cls.UsersDict[DeleteSocket]
        logger.info(f"Disconnect socket: name: {User['name']}\tID: {User['ID']}")
        del cls.UsersDict[DeleteSocket]
        cls.UsersSockets.remove(DeleteSocket)
        cls.send_notification(User['name'], 'sign_out')

    @classmethod
    def login_protocol(cls, socket):
        OpennnigData = json.loads(socket.receive())
        name = OpennnigData['name']
        ID = socket.environ['REMOTE_PORT']
        socket.send(json.dumps({'status': 'NewID', "ID": ID}))
        cls.UsersSockets.add(socket)
        cls.UsersDict[socket] = {'name': name, 'ID': ID}
        logger.info(f"New socket: name: {name}\tID: {ID}")
        cls.send_notification(name, 'sign_in')

    @classmethod
    def send_message_to_all(cls, SenderSocket, message):
        Sender = cls.UsersDict[SenderSocket]
        SenderMessage = message['content']
        SenderID = Sender['ID']
        SenderName = Sender['name']
        logger.info(f"Sending from: {SenderName}\t message: {SenderMessage}")
        jsonData = {'status': 'Message', 'UserId': SenderID, 'UserName': SenderName,
                    'Content': SenderMessage.replace("\n", "<br>")}
        cls.output_To_sockets(jsonData)

    @classmethod
    def send_notification(cls, UserName, StatusMessage):
        jsonData = {'status': 'Login', 'UserName': UserName, 'StatusMessage': StatusMessage}
        cls.output_To_sockets(jsonData)

    @classmethod
    def output_To_sockets(cls, jsonData):
        for socket in cls.UsersSockets:
            socket.send(json.dumps(jsonData))
