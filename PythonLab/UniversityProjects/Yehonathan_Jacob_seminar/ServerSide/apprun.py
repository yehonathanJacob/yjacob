import argparse

from AppLibrary import app

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--port', '-p', help='port to lissen server on', default=8443)
parser.add_argument('--host', help='host to connect server to', default='0.0.0.0')
args = parser.parse_args()

# Configurations:
debug_mode = True
port = args.port  # SSL default port
host = args.host  # localhost default host
certification = 'AppLibrary/cert.pem'
key = 'AppLibrary/key.pem'

if __name__ == '__main__':
	app.run(host=host, debug=debug_mode, port=port, ssl_context=(certification, key))
