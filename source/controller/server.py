import redis

import zmq
import configparser
import requests
import json

import os.path as path
from source.logic.server_storage import *
from source.logic.server_pub import *
from source.logic.server_sub import *

Config_path = path.abspath(path.join(__file__, "../../..")) + "/config/server.ini"
Config = configparser.ConfigParser()
Config.read(Config_path)

server_api_host = Config.get('api', 'host')
server_api_port = Config.get('api', 'port')
server_zmq_host = Config.get('zmq', 'host')
server_zmq_port = Config.get('zmq', 'port')
redis_host = Config.get('redis', 'host')
redis_port = Config.get('redis', 'port')
redis_username = Config.get('redis', 'username')
redis_password = Config.get('redis', 'password')


def chat_server():
	# establishing the redis connection
	r = connect_redis()
	# should also flush the redis in real scenario or properly manage its initiation process
	zmq_socket_server = start_server_zmq_publisher()
	start_apis(r, zmq_socket_server)
