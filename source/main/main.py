# coding=utf-8

import sys
import logging
import os.path as path
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

Project_path = path.abspath(path.join(__file__, "../../.."))
sys.path.insert(0, Project_path)

from source.controller.client import *
from source.controller.server import *

def main(argv):
	# project_path = path.abspath(path.join(__file__, "../../.."))
	# sys.path.insert(0, project_path)
	flags = translate_command_line_arg(argv)
	if flags[0]:
		logging.info("Check 1 [starting server]\n\n")
		chat_server()
	if flags[1]:
		logging.info("Check 2 [starting client]\n\n")
		chat_client()


def translate_command_line_arg(input_argument):

	flags = [False, False, False, False, False, False, False]
	if input_argument[0] == 'start_chat_server_and_client':
		flags = [True, True]
	elif input_argument[0] == 'start_chat_server':
		flags[0] = True
	elif input_argument[0] == 'start_chat_client':
		flags[1] = True
	else:
		print('\n\n invalid command line arguments \n\n')
	return flags


if __name__ == "__main__":
	# Project_path = path.abspath(path.join(__file__, "../../.."))
	# sys.path.insert(0, Project_path)
	main(sys.argv[1:])
