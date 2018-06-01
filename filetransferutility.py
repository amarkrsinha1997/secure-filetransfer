from ftplib import FTP
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import socket
import threading
from crypto import *
from flask import flash, redirect, url_for, request

import app


PORT = 2121
allowed_connection = 256
allowed_connection_per_ip = 5


class MyHandler(FTPHandler):
    def on_file_received(self,filepath):
        decrypt(getkey(), filepath)
        flash("File received", filepath)
        if app.connected:
            return redirect(url_for("sendfile"))
        else:
            return redirect(url_for(request.base_url.split('/')[-1]))

class Server():
    user = None
    password = None

    def __init__(self,username, password):

        if not os.path.exists('sharefolder'):
            os.makedirs('sharefolder')
        self.user = username        
        self.password = password

    def startserver(self):
        # Instantiate a dummy authorizer for managing 'virtual' users
        authorizer = DummyAuthorizer()

        # Define a new user having full r/w permissions and a read-only
        # anonymous user
        authorizer.add_user(self.user, self.password, './sharefolder',msg_login="Login successful.", msg_quit="Goodbye.", perm='elradfmwM')
        authorizer.add_anonymous(os.getcwd())

        # Instantiate FTP handler class
        handler = MyHandler
        handler.authorizer = authorizer

        # Define a customized banner (string returned when client connects)
        handler.banner = "A client is connected with your server."

        # Instantiate FTP server class and listen on 0.0.0.0:2121
        address = ('', PORT)

        server = FTPServer(address, handler)

        # set a limit for connections
        server.max_cons = allowed_connection
        server.max_cons_per_ip = allowed_connection_per_ip

        # start ftp server
        server.serve_forever()


class Client():
    ftp = FTP()
    user = None
    password = None
    
    def __init__(self, user, password, hostname):
        self.ftp.connect(hostname, PORT)
        self.user = user
        self.password = password
        self.status =  self.ftp.login(self.user, self.password)

    def connect(self, filename, file):
        try:
            localfile = encrypt(getkey(), filename, file)  # open the encrypted file
        except Exception as e:
            print(e)
        try:
            print ("[!] File Transfer in Progress....")
            result = self.ftp.storbinary("STOR "+str(os.path.basename("(encrypted)"+fil)),localfile)   # transfer the encrypted file to the FTP server using raw FTP STOR command. Result of the data transfer will be returned
        except Exception as e:
            print(e)     # print any exception occured
        else:
            localfile.close()   # if no exception occured, show the result
            return str(result)
    

   
class IpFinder():
    ips_ng_share = []
    def connect_with_ip(self, ip, port=PORT):
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.settimeout(0.5)
            server_address = (ip, port)
            my_socket.connect(server_address)
            print("connected", ip)
        except Exception as e:
            pass
        else:
            self.ips_ng_share.append(ip)
        finally:
            my_socket.close()

    def break_ip(self, ip):
        parts_4 = ip.split('.')
        return ".".join(parts_4[:3]), parts_4[3]

    def get_all_host(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        my_ip = s.getsockname()[0]
                
        print("My Ip :", my_ip)
        s.close()
        del s
        network_part, my_part = self.break_ip(my_ip)
        print("Wait few minutes scaning for all ther server available here....")
        for x in range(220,240):
            if x == int(my_part):
                continue
            self.connect_with_ip(network_part + "." + str(x))
        return self.ips_ng_share, my_ip
