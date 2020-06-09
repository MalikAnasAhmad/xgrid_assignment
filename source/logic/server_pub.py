import zmq
import configparser
import requests
import json

import os.path as path

Config_path = path.abspath(path.join(__file__, "../../..")) + "/config/server.ini"
Config = configparser.ConfigParser()
Config.read(Config_path)

server_api_host = Config.get('api', 'host')
server_api_port = Config.get('api', 'port')
server_zmq_host = Config.get('zmq', 'host')
server_zmq_port = Config.get('zmq', 'port')

# context = zmq.Context()
# socket = context.socket(zmq.SUB)
# socket.connect('tcp://127.0.0.1:2000')
# socket.setsockopt(zmq.SUBSCRIBE, b'')
#
# while True:
# 	message = socket.recv_pyobj()
# 	print(message)


def start_server_zmq_publisher():
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.bind('tcp://' + server_zmq_host + ':' + server_zmq_port)
	return socket
