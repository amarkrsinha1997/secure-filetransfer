import socket
import threading
import sys
import time, os
from random import randint
# from config import config

#had to make the recv function multithreading and rest normal
PORT = 3238
#globals
ips_ng_share = []
def recv(sock, filename, filesize):

	if filename:
		if not os.path.exists('sharefolder'):
			os.makedirs('sharefolder')
		f = open('sharefolder/'+filename, 'wb')
		totalRecv = 0
		while totalRecv < int(filesize):
			data = sock.recv(4096)
			totalRecv += len(data)
			f.write(data)
		print("\nDownload Complete!")
		f = open('sharefolder/'+filename,"rb")
		return f.read()



class Server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections=[]
	def __init__(self):
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('0.0.0.0', PORT))
		self.sock.listen(1)
		print ('Server Running ...')		
		sThread = threading.Thread(target=self.run)
		sThread.daemon = True
		sThread.start()
		self.sender()


	def handler(self, c, a):
		while True:
			filename = c.recv(1096)
			if not filename:
				self.connections.remove(c)	
				print(self.connections)
				break
			filesize = c.recv(1096)
			data = recv(c, str(filename,'utf-16'), str(filesize,'utf-16'))
			if not filesize:
				self.connections.remove(c)	
				break
			for connection in self.connections:
			
				if connection == c: 
					continue
				connection.send(bytes(filename,'utf-16'))
				connection.send(bytes(filesize,'utf-16'))
				connection.sendall(data)
			


	def sender(self):
		while True:
			try:
				filename = input("Enter the location of the file :")
				f = open(filename, 'rb')
				print(filename)
			except Exception as e:
				continue
					
			data = f.read()
			print(data)
			for connection in self.connections:
				connection.send(bytes(filename,'utf-16'))
				connection.send(bytes(str(os.path.getsize(filename)),'utf-16'))
				print(self.connections)
				connection.sendall(data)
				print(connection)
				


	def run(self):	 
		while True:
			print("Waiting for new connection...")
			c, a = self.sock.accept()
			cThread = threading.Thread(target=self.handler, args=(c, a))
			print(ips_ng_share)
			cThread.daemon = True
			cThread.start()
			self.connections.append(c)
			print("\n",str(a[0]) + ':' + str(a[1]), "connected")



class Client:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	def recv_file(self):
		while True:
			filename = self.sock.recv(1096)
			if not filename: 
				break
			filesize = self.sock.recv(1096)
			if not filesize: 
				break
			try:
				recv(self.sock, str(filename,'utf-16') ,str(filesize,'utf-16'))
			except: 
				sys.exit(0)


	def __init__(self):
		address = self.select_the_host()
		self.sock.connect((address,PORT))
		iThread = threading.Thread(target=self.recv_file)
		iThread.daemon = True
		iThread.start()
				
		while True:
			self.send_file()
		#get the filesize name and save it to sharefolder
		

	def send_file(self):
		filename = input("Enter the location of the file :")
		try:	
			f = open(filename, 'rb')
		except: 
			print("File doesn't exist")
			return
		data = f.read()

		self.sock.send(bytes(filename, 'utf-16'))
		filesize =str(os.path.getsize(filename))
		self.sock.send(bytes(filesize, 'utf-16'))
		self.sock.sendall(data)


	def connect_with_ip(self, ip, port=PORT):
		print(ip)
		try:
			my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			my_socket.settimeout(0.5)
			server_address = (ip, port)
			my_socket.connect(server_address)
			print("connected", ip)
		except Exception as e:
			pass
		else:
			ips_ng_share.append(ip)
		finally:
			my_socket.close()

	def select_the_host(self):
		host_list = self.get_all_host()
		for key, value in enumerate(host_list):
			print(key+1, ".", value)
		serial = int(input("Enter the serial number with which you want to connect :"))
		return host_list[serial-1]


	def break_ip(self, ip):
		parts_4 = ip.split('.')
		return ".".join(parts_4[:3]), parts_4[3]

	def get_all_host(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('google.com', 0))
		my_ip = s.getsockname()[0]
		s.close()
		del s
		network_part, my_part = self.break_ip(my_ip)
		for x in range(227,230):
			if x == my_part:
				continue
			self.connect_with_ip(network_part + "." + str(x))
		return ips_ng_share


answer=input("What you want to be Server or Client?(s/c) :")
if answer == 's':
	server = Server()
elif answer == 'c':
	client = Client()
else:
	print('Wrong choice!')
