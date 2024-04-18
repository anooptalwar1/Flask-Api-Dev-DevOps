import subprocess
import socketio
import os
#from app import app
from flask import Flask, flash, request, redirect, render_template, abort, jsonify, send_from_directory, send_file, safe_join, abort
from flask_socketio import SocketIO, send, emit

app = Flask(__name__, static_folder='static/', template_folder="templates")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None


#sio = socketio.Client()
#sio.connect('http://192.168.1.250:5000')

# pubip_url = "http://www.ip-api.com/json"
# api_call = requests.get(pubip_url)
# data = api_call.json()
# ip = data['query']
# print (ip)

@app.route('/', methods=['GET'])
def home():
	return render_template('ping.html')


#@socketio.on('connect')
#def connect():
#    print("I'm connected!")
#	if not self.authenticate(request.args):
#		raise ConnectionRefusedError('unauthorized!')
#
#@socketio.on('my message')
#def on_message(data):
#    print('I received a message!')


@app.route('/ping', methods=['GET'])
def ping():
    if request.method == 'GET':
        p = subprocess.Popen(["ping.exe","192.168.1.250"], stdout = subprocess.PIPE)
        return p.communicate()[0]
        # list_test = (q.decode('utf-8')).split('\n')
        # ping_res = "0";
        # ss = ""
        # for lt in list_test:
        #     ss+=lt+'\n'
        #     # if "rtt min/avg/max/mdev" in lt:  #rtt min/avg/max/mdev = 0.019/0.025/0.029/0.006 ms
        #     #     buf1 = lt.split(' ')
        #     #     buf2 = buf1[3].split('/') #0.019/0.025/0.029/0.006
        #     #     ping_res = buf2[1]
        #     #     break
        # return ss

@socketio.on('my_ping')
def ping_pong():
	emit('my_pong')


@socketio.on('connect')
def test_connect():
	global thread
	if thread is None:
		thread = socketio.start_background_task(target=background_thread)
	emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
	print('Client disconnected', request.sid)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5234, debug=True)
