#!/usr/bin/env python
import os, sys
from flask import Flask
from flask import request
from flask_negotiate import consumes
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from controllers import procedure_controller

USER = sys.argv[1]
PASSWORD = sys.argv[2]
HOST = sys.argv[3]
PORT = sys.argv[4]
DATABASE = sys.argv[5]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    USER, PASSWORD, HOST, PORT, DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


@app.route('/api/object/names')
def get_all_object_names():
    return procedure_controller.get_all_object_names()


@app.route('/api/procedure/names')
def get_all_procedure_names():
    return procedure_controller.get_all_procedure_names(request)


@app.route('/api/procedure/<int:procedure_id>')
def get_procedure_by_id(procedure_id):
    return procedure_controller.get_procedure_by_id(procedure_id)


@app.route('/api/procedure', methods=['POST'])
@consumes('application/json')
def add_procedure():
    return procedure_controller.add_procedure(request)


@app.route('/api/procedure/<int:procedure_id>', methods=['DELETE'])
def deactivate_procedure(procedure_id):
    return procedure_controller.deactivate_procedure(request, procedure_id)


@app.route('/api/procedure/<int:procedure_id>', methods=['PUT'])
@consumes('application/json')
def update_procedure(procedure_id):
    return procedure_controller.update_procedure(request, procedure_id)


if __name__ == "__main__":
    """ Intialization of Flask server"""
    port = int(os.environ.get('PORT', 5010))
    host = os.environ.get('HOST', '0.0.0.0')
    app.run(host=host, port=port)
