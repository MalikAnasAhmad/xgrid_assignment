import redis
import configparser

import os.path as path

Config_path = path.abspath(path.join(__file__, "../../..")) + "/config/server.ini"
Config = configparser.ConfigParser()
Config.read(Config_path)

redis_host = Config.get('redis', 'host')
redis_port = Config.get('redis', 'port')
redis_username = Config.get('redis', 'username')
redis_password = Config.get('redis', 'password')


def connect():
	r = redis.StrictRedis(host=redis_host, port=int(redis_port), password=redis_password, decode_responses=True)
	return r
