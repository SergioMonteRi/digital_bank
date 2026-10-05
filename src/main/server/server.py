from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from src.database.base import Base
from src.database.connection import db_connection_handler
from src.exceptions.domain.domain_error import DomainError
from src.exceptions.handlers.domain_error_handler import handle_domain_error
from src.exceptions.handlers.http_error_handler import handle_http_error
from src.exceptions.handlers.unexpected_error_handler import handle_unexpected_error
from src.exceptions.handlers.werkzeug_error_handler import handle_werkzeug_error
from src.exceptions.http.http_error import HttpError
from src.main.routes.company_routes import company_routes_bp
from src.main.routes.individual_routes import individual_routes_bp

# pylint: disable=unused-import
from src.models.entities.company import CompanyTable  # noqa: F401
from src.models.entities.individual import IndividualTable  # noqa: F401
from src.models.entities.transaction import TransactionTable  # noqa: F401

# pylint: enable=unused-import


db_connection_handler.connect_to_db()

Base.metadata.create_all(db_connection_handler.get_engine())


app = Flask(__name__)

CORS(app)

app.register_blueprint(individual_routes_bp)
app.register_blueprint(company_routes_bp)


app.register_error_handler(HttpError, handle_http_error)
app.register_error_handler(DomainError, handle_domain_error)
app.register_error_handler(Exception, handle_unexpected_error)
app.register_error_handler(HTTPException, handle_werkzeug_error)
