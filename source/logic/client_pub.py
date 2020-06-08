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


def scan_user_input_and_post_it_to_server_for_publishing(client_id, thread_subscription_messages):
	message = {"client_id": client_id, 'user_input': None}
	while True:
		user_input = input(client_id + " : ")
		message['user_input'] = user_input

		server_url = 'http://' + server_api_host + ':' + server_api_port + '/' + 'user_input'
		query = json.dumps(message)
		requests.post(server_url, query)
		if user_input == 'exit()':
			exit_server(client_id)
			thread_subscription_messages.join()  # kill the thread for zmq subscription
			break
