#!/usr/bin/env python
import subprocess
import os
#from app import app
from flask import Flask, flash, request, redirect, render_template, abort, jsonify, send_from_directory, send_file, safe_join, abort
from flask_socketio import SocketIO, send, emit

async_mode = None
app = Flask(__name__, static_folder='static/', template_folder="templates")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None


@app.route('/', methods=['GET'])
def home():
	return render_template('ping.html')

@app.route('/ping', methods=['GET'])
def ping():
    if request.method == 'GET':
        p = subprocess.Popen(["ping.exe","192.168.1.250"], stdout = subprocess.PIPE)
        return p.communicate()[0]


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
