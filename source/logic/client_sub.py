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


def join_server(client_id):
	message = {"client_id": client_id}
	server_url = 'http://' + server_api_host + ':' + server_api_port + '/' + 'join_chat'
	query = json.dumps(message)
	response = requests.post(server_url, query)
	response_json = response.json()
	result = response_json['available']
	return result
	# check if the same id exist or not
	# check if the number of subscribers are less than 100


def print_all_of_the_previous_chat():
	# it should be accompnied with a time stamp
	server_url = 'http://' + server_api_host + ':' + server_api_port + '/' + 'previous_chat'
	response = requests.get(server_url)
	response_json = response.json()
	if bool(response_json['chat']):
		print(response_json['chat'])


def exit_server(client_id):
	message = {"client_id": client_id}
	server_url = 'http://' + server_api_host + ':' + server_api_port + '/' + 'exit_chat'
	query = json.dumps(message)
	response = requests.post(server_url, query)
	response_json = response.json()
	result = response_json['left']
	return result
# remove the client_id from the list
# unsubscribe the server zmq
# shut down the client zmq


def subscribe_to_server():
	context = zmq.Context()
	socket = context.socket(zmq.SUB)
	socket.connect(server_zmq_host + ':' + server_zmq_port)
	socket.setsockopt(zmq.SUBSCRIBE, b'')

	while True:
		message = socket.recv_pyobj()
		print(message)
