import socket
import sys
import os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Create a TCP/IP socket
server_ip = input('Enter server IP : ')
rep = os.system('ping ' + server_ip)
if rep == 0:
	print ('n n server is up n n')
else:
	print ('server is down')