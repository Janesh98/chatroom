import socket
import threading
ip_addr = '0.0.0.0'
port = 8000
print("Server Started")

# setup 32bit ipv4, TCP/IP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_running = True

# give the socket an ip address and port
socket_details = (ip_addr, port)
serversocket.bind(socket_details)
serversocket.listen(100)

# store the connected devices
connected_devices = {}

# functopn to start a client thread
def start_client_thread(connection, address):
	# client_thread(conn, addr)
	th = threading.Thread(target=client_thread, args=(connection, address))
	th.start()
	connected_devices[conn]['thread'] = th

# broadcast funcction, send data to all clients (except the original sender)
def broadcast(message, conn):
	# loop through connected devices
	# send data to connection
	for conn in connected_devices:
		if conn != original_conn:
			conn.send(message)

# function to handle client connection thread
def client_thread(conn, addr):
	welcome = "welcome to the chatroom"
	conn.send(welcome.encode())

	# if the client sends us data
	# send the data to every other client
	while server_running:
		try:
			message = conn.recv(1024)
			if message:
				enc_message = message.decode()
				print("<{}> {}".format(addr, enc_message))
				print(message_to_send)
				broadcast(message_to_send, conn)
			else:
				pass
				# print("<{}> has left the chat".format(addr))
		except:
			continue

# main loop
# loop forever
# if theres a client waiting to connect
# make a thread for the client
# goto 1
try:
	while True:
		conn, addr = serversocket.accept()
		connected_devices[conn] = {'addr' : addr}
		print("{} connected".format(addr))
		# start a thread for the client connection
		start_client_thread(conn, addr)

except KeyboardInterrupt:
	print('Server Shutting Down')
	for conn in connected_devices:
		conn.close()
	serversocket.close()
	server_running = False
	print('Goodbye')
	sys.exit(0)
