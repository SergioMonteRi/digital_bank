from flask import Flask
from flask_cors import CORS

from src.database.connection import db_connection_handler

db_connection_handler.connect_to_db()

app = Flask(__name__)

CORS(app)
