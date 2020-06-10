import threading
import sys
import logging
import atexit
from source.logic.client_pub import *
from source.logic.client_sub import *
from source.logic.client_handshake_management import *


def chat_client():

	client_id = create_id()

	# commenting the following line temporarily
	# atexit.register(exit_server(client_id)) # run the code on the exit of the terminal
	# zmq_socket = start_client_zmq_publisher(client_id)  # don't need it in case where full client to server
	# communication is done via API and server to clients message communication is mostly done via zeroMQ
	try:
		if bool(join_server(client_id)):
			print_all_of_the_previous_chat(client_id)
			# thread_subscription_messages = threading.Thread(target=subscribe_to_server, args=(1,))
			thread_subscription_messages = threading.Thread(target=subscribe_to_server,args=(client_id,))
			thread_subscription_messages.start()
			# scan the input data from the client user and send it to server so that it can publish/broadcast to all other
			# clients
			## thread_user_input = threading.Thread(target=scan_user_input_and_post_it_to_server_for_publishing
			## (client_id, thread_subscription_messages), args=(1,))
			## thread_user_input.start()
			# the above three lines are not equired the first thread should run separately this thrfead must be
			# conclusive in terms of client being alive or not
			scan_user_input_and_post_it_to_server_for_publishing(client_id)

			# thread_subscription_messages.setDaemon(True)
			# quit(thread_subscription_messages)
			# quit()
			# raise SystemExit
			# sys.exit()
			# in case the code is terminated non gracefully or it crashes, make sure to run exit_server function
		elif join_server(client_id) is None:
			print("service is not available for now")
		else:
			print(client_id, " : You are not allowed to join")
	except Exception as e:
		logging.error(e)
		exit_server(client_id)
