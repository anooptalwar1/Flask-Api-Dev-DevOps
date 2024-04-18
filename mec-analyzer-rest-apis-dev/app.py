#!/usr/bin/env python
import os
from flask import Flask, request, Response, abort, jsonify, send_from_directory
import json
from PIL import Image
from controllers import database_controller
from constants import app_constants
from flask_cors import CORS
from flask_socketio import SocketIO, send
import datetime
from datetime import datetime
import time
import socket as web_socket

if not os.path.exists(app_constants.FILE_UPLOAD_DIRECTORY):
    os.makedirs(app_constants.FILE_UPLOAD_DIRECTORY)


api = Flask(__name__)
CORS(api)
socketio = SocketIO(api, cors_allowed_origins="*")


"""List files on the server."""
@api.route("/api/mec/files", methods=["GET"])
def list_files():
    filesize = []
    for filename in os.listdir(app_constants.FILE_UPLOAD_DIRECTORY):
        path = os.path.join(app_constants.FILE_UPLOAD_DIRECTORY, filename)
        file_stats = os.stat(path)
        if os.path.isfile(path):
            # files.append(filename)
            file_stats = os.stat(path)
            sizebyte = str(int(file_stats.st_size / (1024 * 1024))) + "MB"
            # sizebyte = file_stats.st_size / (1024 * 1024)
            filesize.append({'filename':filename,'filesize': sizebyte})
    return jsonify(filesize)



"""Download a file or return the names of file on server."""
@api.route("/api/mec/files/<filename>", methods=["GET"])
def get_file(filename):
    return send_from_directory(app_constants.FILE_UPLOAD_DIRECTORY, filename, as_attachment=True)


"""Upload a file."""
@api.route("/api/mec/files/<filename>", methods=["POST"])
def post_file(filename):

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "do not create a new dir")

    with open(os.path.join(app_constants.FILE_UPLOAD_DIRECTORY, "tempFile"), "wb") as fp:
        fp.write(request.data)

    # os.remove(app_constants.FILE_UPLOAD_DIRECTORY + "/tempfile")

    return jsonify({"message":"File has been uploaded successfully"}), 201


"""Convert a file from png to jpg"""
@api.route("/api/mec/files/convert", methods=['GET', 'POST'])
def convert():
    if request.method == 'GET':
        filestats = os.stat('resources/PNG_3MB.png')
        sizemb = str(round(filestats.st_size / 1024)) + "KB"
        ConvertStart = time.time()
        im = Image.open("resources/PNG_3MB.png")
        im = im.convert('RGB')
        im.save('resources/im_as_jpg_3MB.jpg', quality=100)
        ConvertStop = time.time()
        computetime = int((ConvertStop - ConvertStart)* 1000)
        return jsonify({"conversionTime": computetime, "filesize" : sizemb }), 200
    if request.method == 'POST':
        # retrieve date and time
        folder_time = str(datetime.now().timestamp()).replace(".","")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # calculate received file size
        file.seek(0, os.SEEK_END)
        filesize = file.tell()
        # conditions to check rceived file format
        if (str(file).find('.PNG') != -1) or (str(file).find('.png') != -1):
            Convert_Start = time.time()
            im = Image.open(file)
            im = im.convert('RGB')
            im.save(folder_time + '.jpg', quality=100)
            Convert_Stop = time.time()
            compute_time = int((Convert_Stop - Convert_Start)* 1000)
            os.remove(folder_time + '.jpg')
        elif (str(file).find('.JPG') != -1) or (str(file).find('.jpg') != -1) or (str(file).find('.jpeg') != -1):
            Convert_Start = time.time()
            im = Image.open(file)
            im = im.convert('RGB')
            im.save(folder_time + '.png', quality=100)
            Convert_Stop = time.time()
            compute_time = int((Convert_Stop - Convert_Start)* 1000)
            os.remove(folder_time + '.png')
        else:
            return jsonify("Send files in jpg or png format")
    return jsonify({"conversionTime": compute_time , "receivedFilesize": str(round(filesize / 1024)) + "KB" }), 200


""" Insert a record in MongoDB collection. """
@api.route("/api/mec/records", methods=["POST"])
def post_record():
    request_data = request.get_json()
    database_controller.insert_record(request_data)
    response = Response("", status=201)
    return response


""" Fetches all MEC Reports records from MongoDB collection. """
@api.route("/api/mec/records", methods=["GET"])
def find_all_records():
    return Response(database_controller.find_all_records(), status=200, mimetype='application/json')


""" Fetches MEC Reports records for specified deviceId from MongoDB collection. """
@api.route("/api/mec/records/<string:deviceId>", methods=["GET"])
def find_records_by_device_id(deviceId):
    return Response(database_controller.find_records_by_device_id(deviceId), status=200, mimetype='application/json')


""" Deletes all MEC Reports records from MongoDB collection. """
@api.route("/api/mec/records", methods=["DELETE"])
def delete_records():
    return Response(database_controller.delete_all_records(), status=200, mimetype='application/json')


""" Fetches MEC Client Portal IP address. """
@api.route("/api/mec/clientIp", methods=["GET"])
def fetch_mec_client_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return jsonify({'clientIp': "{}:{}".format(request.remote_addr, request.environ.get('REMOTE_PORT'))}), 200
    else:
        return jsonify({'clientIp': "{}:{}".format(request.environ['HTTP_X_FORWARDED_FOR'], request.environ.get('REMOTE_PORT'))}), 200


# TCP Socket connecetion
""" Listner for clients to broadcast it with timestamp"""
@socketio.on('calculate_latency')
def handlemsg():
    # newstring = msg + datetime.datetime.now(datetime.timezone.utc)
    socketio.emit('calculate_latency')


# UDP Socket
def configure_udp_socket(ip, port):
    udp_socket = web_socket.socket(web_socket.AF_INET, web_socket.SOCK_DGRAM)
    udp_socket.bind((ip, port))

    while True:
        # returns the data as well as the address of the client from which it was sent.
        data, address = web_socket.recvfrom(4096)
        if data:
            sent = web_socket.sendto(data, address)


if __name__ == "__main__":
    port = int(os.environ.get('HOST', 5210))
    host = os.environ.get('HOST', '0.0.0.0')
    
    # api.run(host='0.0.0.0', port=5210, debug=True)

    # In case of TCP socket
    socketio.run(host=host, app=api, port=port, debug=True)

    # #In case of UDP Protocol
    # configure_udp_socket('0.0.0.0',5210)
