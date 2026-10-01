from flask import Flask
from flask_cors import CORS

from src.database.connection import db_connection_handler
from src.exceptions.domain.domain_error import DomainError
from src.exceptions.handlers.domain_error_handler import handle_domain_error
from src.exceptions.handlers.http_error_handler import handle_http_error
from src.exceptions.handlers.unexpected_error_handler import handle_unexpected_error
from src.exceptions.http.http_error import HttpError

db_connection_handler.connect_to_db()

app = Flask(__name__)

CORS(app)

app.register_error_handler(HttpError, handle_http_error)
app.register_error_handler(DomainError, handle_domain_error)
app.register_error_handler(Exception, handle_unexpected_error)
