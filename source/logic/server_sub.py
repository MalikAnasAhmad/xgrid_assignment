import datetime
import logging
import json
import sys
import time
import zmq
import configparser
import requests
from flask import Flask, request
import os.path as path

from source.logic.redis import *
from source.logic.server_pub import *
Config_path = path.abspath(path.join(__file__, "../../..")) + "/config/server.ini"
Config = configparser.ConfigParser()
Config.read(Config_path)

server_api_host = Config.get('api', 'host')
server_api_port = Config.get('api', 'port')
no_of_messages_to_be_sent_to_client = Config.get('client', 'no_of_messages')

list_of_client_ids = []


def join_group_chat(client_id, message, zmq_socket_server):
	# put client_id in the list
	# announce the joining of the client_id via publish
	list_of_client_ids.append(client_id)

	epoch_time = int(time.time())

	# print('\n\n\n',epoch_time,'\n\n\n')
	# epoch_time = int(float(time.time()))
	# message_to_be_published = client_id + " : " + message+"\n"+datetime.datetime.fromtimestamp(time)+'\n\n'
	# message_to_be_published = {'user_id': client_id, 'time': str(epoch_time), 'message': message}#temp

	message_to_be_published = '\n\n' + client_id + ' has joined the group @ ' +\
							  str(datetime.datetime.fromtimestamp(epoch_time))+ '\n\n'

	publish_on_message_broker(zmq_socket_server, message_to_be_published)#temp
	# publish_on_message_broker(zmq_socket_server, message_to_be_published)


def start_apis(r, zmq_socket_server):
	server_api = Flask(__name__)

	@server_api.route('/join_chat', methods=['POST'])
	def join_chat():
		response_to_the_client = {"approval": None}
		try:
			# query_input = {'wo_id': request.json.get('wo_id'), 'asset_id':
			query_input = {'client_id': request.get_json()['client_id']}
			client_id = query_input['client_id']
			# check if the same id exist or not
			# check if the number of subscribers are less than 100

			# if len(list_of_client_ids) == 100 and client_id not in list_of_client_ids:
			if len(list_of_client_ids) == 0:
				message = client_id + ' is the first person to join the group'
				join_group_chat(client_id, message, zmq_socket_server)
				response_to_the_client['approval'] = 'yes'
			elif len(list_of_client_ids) < 100 and client_id not in list_of_client_ids:
				message = client_id + ' is requesting to join the group'
				join_group_chat(client_id, message, zmq_socket_server)
				response_to_the_client['approval'] = 'conditional'
			# check if he can mention any existing id
			else:
				response_to_the_client['approval'] = 'no'
			return response_to_the_client
		# return json.dumps(response_to_the_client)
		except Exception as e:
			logging.error(e)
			logging.critical("Unexpected error:" + str(sys.exc_info()[0]))
			content = {'status': 'internal server error'}
			return json.dumps(content), 500

	@server_api.route('/verify_referral', methods=['POST'])
	def verify_referral():
		response_to_the_client = {"approval": None}
		try:
			query_input = {'client_id': request.get_json()['client_id'],'user_input': request.get_json()['user_input']}
			client_id = query_input['client_id']
			user_input = query_input['user_input']
			# check if the same id exist or not
			# print('\n\n list_of_client_ids ==> ', list_of_client_ids)
			if user_input in list_of_client_ids:
				response_to_the_client['approval'] = 'yes'
				message = client_id + ' has also joined the group'
				join_group_chat(client_id, message, zmq_socket_server)
			else:
				response_to_the_client['approval'] = 'no'
			return response_to_the_client
			# return json.dumps(response_to_the_client)
		except Exception as e:
			logging.error(e)
			logging.critical("Unexpected error:" + str(sys.exc_info()[0]))
			content = {'status': 'internal server error'}
			return json.dumps(content), 500

	@server_api.route('/previous_chat', methods=['POST'])
	def previous_chat():
		last_few_messages = None
		# try:
		# query_input = {'client_id': request.json.get('client_id')}#temp
		query_input = {'client_id': request.get_json()['client_id']}
		client_id = query_input['client_id']
		print('CLIENT ID in PREVIOUS CHAT API', client_id)
		if client_id in list_of_client_ids:
			# pull last available 100 messages and reply
			# last_few_messages = None
			last_few_messages = get_last_few_messages_from_data_store(r, no_of_messages_to_be_sent_to_client)
			return json.dumps(last_few_messages)
		else:
			return json.dumps(last_few_messages), 401
		# except Exception as e:
		# 	logging.error(e)
		# 	logging.critical("Unexpected error:" + str(sys.exc_info()[0]))
		# 	content = {'status': 'internal server error'}
		# 	return json.dumps(content), 500

	@server_api.route('/user_input_broadcast', methods=['POST'])
	def user_input_broadcast():
		response_to_the_client = {"posted": None}
		try:
			# query_input = {'client_id': request.json.get('client_id'), 'user_input': request.json.get('user_input')}#temp

			query_input = {'client_id': request.get_json()['client_id'], 'user_input': request.get_json()['user_input']}
			# print(query_input)
			client_id = query_input['client_id']
			user_input = query_input['user_input']
			epoch_time = int(time.time())
			if user_input == 'exit()':
				message_to_be_published = client_id + " : " + "IS LEAVING THE GROUP CHAT GROUP\n" + \
										  str(datetime.datetime.fromtimestamp(epoch_time)) + '\n\n'
			else:
				# message_to_be_published = {'user_id': client_id, 'time': str(epoch_time), 'message': user_input}#temp
				message_to_be_published = client_id+ " : "+ user_input+ "\n"+\
										  str(datetime.datetime.fromtimestamp(epoch_time))+ '\n\n'

			publish_on_message_broker(zmq_socket_server, message_to_be_published)
			if user_input != 'exit()':
				chat_storage(r, client_id, user_input, epoch_time)
			# following flag should be set on the result of zmq
			response_to_the_client["posted"] = True

			return json.dumps(response_to_the_client)
		except Exception as e:
			logging.error(e)
			logging.critical("Unexpected error:" + str(sys.exc_info()[0]))
			content = {'status': 'internal server error'}
			return json.dumps(content), 500

	@server_api.route('/exit_chat', methods=['POST'])
	def exit_chat():
		response_to_the_client = {'left': None}
		try:
			# query_input = {'client_id': request.json.get('client_id')}#temp
			query_input = {'client_id': request.get_json()['client_id']}

			client_id = query_input['client_id']
			# remove the client_id from the list
			print('list_of_client_ids =>',list_of_client_ids)
			list_of_client_ids.remove(client_id)
			response_to_the_client['left'] = True
			return json.dumps(response_to_the_client)
		except Exception as e:
			logging.error(e)
			logging.critical("Unexpected error:" + str(sys.exc_info()[0]))
			return json.dumps(response_to_the_client), 500

	server_api.run(host=server_api_host, port=int(server_api_port), threaded=True)
