import logging
from source.logic.client_sub import *

Config_path = path.abspath(path.join(__file__, "../../..")) + "/config/server.ini"
Config = configparser.ConfigParser()
Config.read(Config_path)

server_api_host = Config.get('api', 'host')
server_api_port = Config.get('api', 'port')


# from time import sleep

# context = zmq.Context()
# socket = context.socket(zmq.PUB)
# socket.bind('tcp://127.0.0.1:2000')
#
# messages = [100, 200, 300]
# curMsg = 0
#
# while True:
# 	sleep(1)
# 	socket.send_pyobj({curMsg: messages[curMsg]})
#
# 	if curMsg == 2:
# 		curMsg = 0
# 	else:
# 		curMsg = curMsg + 1


def start_client_zmq_publisher(client_id):
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.bind('tcp://' + client_id)
	return socket
	# socket.send_pyobj({curMsg: messages[curMsg]})


def scan_user_input_and_post_it_to_server_for_publishing(client_id):
	message = {"client_id": client_id, 'user_input': None}
	while True:
		# user_input = input(client_id + " : ")#temp
		# prompt = client_id + " : "
		prompt = ''
		user_input = input(prompt)
		if user_input != 'exit()':
			# print('\033[1A' + prompt + '\033[K')
			print('\033[1A' + '\033[K')
		message['user_input'] = user_input

		server_url = 'http://' + server_api_host + ':' + server_api_port + '/' + 'user_input_broadcast'
		# query = json.dumps(message)#temp
		query = message
		response = requests.post(server_url, json=query)
		if not response.json()['posted']:
			logging.critical("message is not broadcast to others")
		if user_input == 'exit()':
			exit_server(client_id)
			# thread_subscription_messages.join()  # kill the thread for zmq subscription
			break
