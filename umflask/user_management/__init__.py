import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_cors import CORS

USER = sys.argv[1]
PASSWORD = sys.argv[2]
HOST = sys.argv[3]
PORT = sys.argv[4]
DATABASE = sys.argv[5]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    USER, PASSWORD, HOST, PORT, DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
socketio = SocketIO(app)
