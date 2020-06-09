import socket


def is_port_in_use(port):
	import socket
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		return s.connect_ex(('', port)) == 0


# should be put in logic folder
def create_id():
	client_id = None
	port = input("enter your port [port must be in numeric integer and in between 1024 and 5000]: ")

	if port.isdigit() and 1024 <= int(port) <= 5000:
		result = is_port_in_use(int(port))

		hostname = socket.gethostname()
		ip_address = socket.gethostbyname(hostname)

		client_id = ip_address + ':' + port

		if result:
			print("client_id : ", client_id, " is not available use another port number")
			return client_id
		else:
			print("your client_id is : ", client_id)
	else:
		print("invalid port ")
	return client_id
