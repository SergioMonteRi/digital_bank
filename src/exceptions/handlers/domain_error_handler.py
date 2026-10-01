# src/exceptions/handlers/domain_error_handler.py
from src.exceptions.domain.company_not_found import CompanyNotFound
from src.exceptions.domain.domain_error import DomainError
from src.exceptions.domain.individual_not_found import IndividualNotFound
from src.exceptions.domain.insufficient_balance import InsufficientBalance
from src.exceptions.domain.withdrawal_limit_exceeded import WithdrawalLimitExceeded
from src.exceptions.http.http_bad_request import HttpBadRequestError
from src.exceptions.http.http_error import HttpError
from src.exceptions.http.http_not_found import HttpNotFoundError
from src.exceptions.http.http_unprocessable_entity import HttpUnprocessableEntityError

from .http_error_handler import handle_http_error

DOMAIN_TO_HTTP: dict[type[DomainError], HttpError] = {
    IndividualNotFound: HttpNotFoundError("Individual not found"),
    CompanyNotFound: HttpNotFoundError("Company not found"),
    InsufficientBalance: HttpUnprocessableEntityError(
        "Insufficient balance", errors=None
    ),
    WithdrawalLimitExceeded: HttpUnprocessableEntityError(
        "Withdrawal limit exceeded", errors=None
    ),
}


def handle_domain_error(error: DomainError):
    http_error = DOMAIN_TO_HTTP.get(
        type(error), HttpBadRequestError("Business rule violation")
    )

    return handle_http_error(http_error)
