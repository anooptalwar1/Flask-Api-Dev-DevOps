import os
#import magic
import urllib.request
import random
import string
from datetime import datetime
import subprocess
from flask_cors import CORS
#from app import app
from flask import Flask, flash, request, redirect, render_template, abort, jsonify, send_from_directory, send_file, safe_join, abort
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static/', template_folder="templates")
CORS(app)
static_folder_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "client")


UPLOAD_FOLDER = '/app/uploads'
app.secret_key = os.urandom(24)

ALLOWED_EXTENSIONS = set(['txt', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mpeg', 'mp4'])



def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def upload_form():
	return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		folder_time = str(datetime.now().timestamp()).replace(".","")
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(UPLOAD_FOLDER, folder_time+"_"+filename))
			flash('File successfully uploaded')
			return jsonify(folder_time+"_"+filename)
		else:
			flash('Allowed file types are txt, doc, docx, ppt, pptx, xls, xlsx, pdf, png, jpg, jpeg, gif, mpeg, mp4')
			return redirect(request.url)



@app.route('/file-downloads/', methods=['GET'])
def file_downloads():
	if request.method == 'GET':
		try:
			return render_template('downloads.html')
		except Exception as e:
			return str(e)

@app.route('/return-files/<filename>', methods=['GET', 'POST'])
def return_files_tut(filename):
	if request.method == 'GET':
		try:
			return send_from_directory(directory=UPLOAD_FOLDER, filename=filename, as_attachment=True, attachment_filename=(str(filename)))
		except Exception as e:
			return str(e)

@app.route('/delete_item/<filename>', methods=['DELETE'])
def delete_item(filename):
	try:
		os.remove(os.path.join(UPLOAD_FOLDER, filename))
		return jsonify(filename+" "+"Deleted")
	except Exception as e:
		return str(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5678, debug=True)
