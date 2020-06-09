import zmq
import configparser
import requests
import json
import datetime
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
	query = message

	response = requests.post(server_url, json=query)
	response_json = response.json()
	print('response_json in JOIN_SERVER FUNCTION', response_json)
	result = response_json['available']
	print('result =>', result)
	return result


def print_all_of_the_previous_chat(client_id):
	# it should be accompanied with a time stamp
	message = {"client_id": client_id}
	server_url = 'http://' + server_api_host + ':' + server_api_port + '/' + 'previous_chat'
	query = message
	response = requests.post(server_url, json=query)
	response_json = response.json()
	if bool(response_json):
		for chat_message in response_json:
			print(chat_message['user_id'], ":", chat_message['message'], "\n",
				  datetime.datetime.fromtimestamp(int(float(chat_message['time']))), '\n\n')


def exit_server(client_id):
	message = {"client_id": client_id}
	server_url = 'http://' + server_api_host + ':' + server_api_port + '/' + 'exit_chat'
	# query = json.dumps(message)#temp
	query = message
	response = requests.post(server_url, json=query)
	response_json = response.json()
	result = response_json['left']
	return result
	# remove the client_id from the list


def subscribe_to_server(client_id):
	context = zmq.Context()
	socket = context.socket(zmq.SUB)
	# print('\n\n','SERVER ADDRESS',server_zmq_host + ':' + server_zmq_port)
	socket.connect('tcp://' + server_zmq_host + ':' + server_zmq_port)
	socket.setsockopt(zmq.SUBSCRIBE, b'')

	while True:

		message = socket.recv_string()#.recv_pyobj()
		print(message)
		first_word =client_id + " : " + "IS LEAVING THE GROUP CHAT GROUP"
		second_word=message.split('\n', 1)[0]
		if first_word == second_word:
			break
