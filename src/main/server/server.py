from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from src.database.connection import db_connection_handler
from src.exceptions.domain.domain_error import DomainError
from src.exceptions.handlers.domain_error_handler import handle_domain_error
from src.exceptions.handlers.http_error_handler import handle_http_error
from src.exceptions.handlers.unexpected_error_handler import handle_unexpected_error
from src.exceptions.handlers.werkzeug_error_handler import handle_werkzeug_error
from src.exceptions.http.http_error import HttpError
from src.main.routes.individual_routes import individual_routes_bp

db_connection_handler.connect_to_db()

app = Flask(__name__)

CORS(app)

app.register_blueprint(individual_routes_bp)

app.register_error_handler(HttpError, handle_http_error)
app.register_error_handler(DomainError, handle_domain_error)
app.register_error_handler(Exception, handle_unexpected_error)
app.register_error_handler(HTTPException, handle_werkzeug_error)
