import logging
import json
import sys
from flask import Flask, request
import zmq
import configparser
import requests
import os.path as path


Config_path = path.abspath(path.join(__file__, "../../..")) + "/config/server.ini"
Config = configparser.ConfigParser()
Config.read(Config_path)

server_api_host = Config.get('api', 'host')
server_api_port = Config.get('api', 'port')


def start_apis(r):
	server_api = Flask(__name__)
	@server_api.route('/previous_chat', methods=['GET'])
	def previous_chat():
		try:
			# pull last available 100 messages and reply
			last_100_messages = None

			return last_100_messages
		except Exception as e:
			logging.error(e)
			logging.critical("Seems like an issue with reading memcache or input message")
			logging.critical("Unexpected error:" + str(sys.exc_info()[0]))
			content = {'status': 'internal server error'}
			return json.dumps(content), 500
	server_api.run(host=server_api_host, port=int(server_api_port), threaded=True)
