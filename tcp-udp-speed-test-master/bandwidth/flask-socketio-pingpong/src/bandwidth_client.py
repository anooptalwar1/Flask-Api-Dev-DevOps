import datetime
import socket
import os
import subprocess, platform

HOST = '127.0.0.1'
PORT = 50000
BUFFER = 4096

testdata = b'x' * BUFFER * 4

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))
for i in range(1, 1000000):
    sock.send(testdata)
sock.close()


def ping(host):
    """
    Returns True if host responds to a ping request
    """
    import subprocess, platform

    # Ping parameters as function of OS
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + host
    need_sh = False if  platform.system().lower()=="windows" else True

    # Ping
    return subprocess.call(args, shell=need_sh) == 0

# test call
print(ping("127.0.0.1"))