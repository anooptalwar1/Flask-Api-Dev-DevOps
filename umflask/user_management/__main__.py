import json
import os
from user_management import socketio
from user_management import app
from flask import request
from flask_negotiate import consumes
from flask_socketio import disconnect
from user_management.controllers import api_controller
from user_management.controllers import socket_controller
from user_management.constants import db_constants


@app.route('/api/user', methods=['POST'])
@consumes('application/x-www-form-urlencoded')
def insert_user():
    return api_controller.insert_user(request)


@app.route('/api/user/login', methods=['POST'])
@consumes('application/x-www-form-urlencoded')
def login():
    return api_controller.login(request)


@app.route('/api/user', methods=['GET'])
def get_all_users_for_user_id():
    """ API endpoint to fetch users for CMS portal """
    return api_controller.get_all_users_for_user_id(request)


@app.route('/api/user', methods=['PUT'])
@consumes('application/x-www-form-urlencoded')
def update_user():
    """ API endpoint to update a user's details """
    return api_controller.update_user(request)


@app.route('/api/user', methods=['DELETE'])
@consumes('application/x-www-form-urlencoded')
def deactivate_user():
    """ API endpoint to deactivate a user """
    return api_controller.deactivate_user(request)


@socketio.on('disconnect')
def on_disconnect():
    """ Socket event called a connected socket disconnected """
    ip_address = "{}:{}".format(
        request.remote_addr, request.environ.get('REMOTE_PORT'))
    device_type = socket_controller.set_status_offline(ip_address)
    if device_type:
        if device_type == db_constants.SESSION_DEVICE_TYPE_ENUM_HOLOLENS:
            get_online_hololens_users()
        else:
            get_online_android_users()


@socketio.on('update_session')
def update_session(json_data):
    """ Socket event invoked when connected socket send updated session data """
    ip_address = "{}:{}".format(
        request.remote_addr, request.environ.get('REMOTE_PORT'))
    response, device_type = socket_controller.update_session(
        ip_address, json_data)
    if device_type:
        if device_type == db_constants.SESSION_DEVICE_TYPE_ENUM_HOLOLENS:
            get_online_hololens_users()
        else:
            get_online_android_users()
    return response


@socketio.on('get_online_hololens_users')
def get_online_hololens_users():
    """ Socket event invoked when connected socket needs online HoloLens users """
    users = socket_controller.get_online_hololens_users()
    socketio.emit('online_hololens_users', json.dumps(users, default=str))


@socketio.on('get_online_android_users')
def get_online_android_users():
    """ Socket event invoked when connected socket needs online Android users """
    users = socket_controller.get_online_android_users()
    socketio.emit('online_android_users', json.dumps(users, default=str))


def main():
    """ Intialization of Flask server with SocketIO """
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    socketio.run(host=host, app=app, port=port, debug=True)
