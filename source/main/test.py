print('16'.isdigit())
print('16.9'.isdigit())

import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IPAddr)

# print(client_id.rsplit(':',1))