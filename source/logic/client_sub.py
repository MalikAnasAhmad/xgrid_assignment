import zmq
import configparser
import requests
import logging
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


def ask_user_for_pointing_out_an_existing_user(client_id):
	message = {"client_id": client_id, 'user_input': None}
	prompt = "You are required to mention one id which has already joined the group chat : "
	user_input = input(prompt)
	message['user_input'] = user_input

	server_url = 'http://' + server_api_host + ':' + server_api_port + '/' + 'verify_referral'
	# query = json.dumps(message)#temp
	query = message
	response = requests.post(server_url, json=query)

	if response.json()['approval'] == 'yes':
		return True
	else:
		return False


def join_server(client_id):
	result=None
	message = {"client_id": client_id}
	server_url = 'http://' + server_api_host + ':' + server_api_port + '/' + 'join_chat'
	query = message

	response = requests.post(server_url, json=query)
	response_json = response.json()
	approval = response_json['approval']
	if approval == 'yes':
		result=True
	elif approval == 'conditional':
		result = ask_user_for_pointing_out_an_existing_user(client_id)
	elif approval == 'no':
		result=False
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
		first_word = client_id + " : " + "IS LEAVING THE GROUP CHAT GROUP"
		second_word = message.split('\n', 1)[0]
		if first_word == second_word:
			break
