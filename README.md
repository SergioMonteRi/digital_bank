# Digital Bank

A REST API for a digital bank, built with Flask. It supports two kinds of clients, individuals and companies, with account creation, lookup, deposits, withdrawals and statements.

## Tech stack

- **Python 3.14**, **Flask 3**
- **SQLAlchemy 2** (ORM) with SQLite
- **Pydantic 2** for request validation and response serialization
- **pytest**, **ruff**, **pylint** and **pre-commit**

## Architecture

The code is organized in layers, each depending only on the one below it through interfaces:

```text
routes → views → controllers → services → repositories → entities
```

- **Views** validate HTTP input and shape responses.
- **Controllers** connect views to services.
- **Services** hold the business rules: withdrawal limits and balance checks.
- **Repositories** handle persistence.
- **Composers** wire the layers together for each route (dependency injection).

## Highlights

- **Safe money handling:** amounts use `Decimal` and `Numeric(12, 2)` instead of `float`, so values never drift by fractions of a cent. Withdrawal limits are rounded down to the cent.
- **Atomic, race-safe transactions:** the balance update and the statement entry are written in a single database transaction. Withdrawals use a conditional `UPDATE ... WHERE balance >= amount`, so concurrent requests cannot overdraw an account.
- **Thread-safe sessions:** each request gets its own SQLAlchemy session through a context manager.
- **Input validation:** email format, phone pattern, minimum age, non-negative income, no blank strings. Unknown fields are rejected with `422`.
- **Consistent errors:** domain errors (not found, insufficient balance, limit exceeded) are mapped to HTTP responses with a stable JSON format.
- **App factory:** `create_app(config)` builds the application, so tests can create apps with different settings.
- **Configuration through environment variables:** `DATABASE_URL` and `FLASK_DEBUG`.

## API

Each endpoint below exists for both client types: `/individuals` and `/companies`.

| Method | Path | Description | Success |
| --- | --- | --- | --- |
| `POST` | `/individuals` | Create a client | `201` |
| `GET` | `/individuals/<id>` | Get a client | `200` |
| `POST` | `/individuals/<id>/deposit` | Deposit `{"amount": "100.00"}` | `204` |
| `POST` | `/individuals/<id>/withdraw` | Withdraw `{"amount": "50.00"}` | `204` |
| `GET` | `/individuals/<id>/statement` | List transactions, newest first | `200` |

Business rules:

- Individuals can withdraw up to **70%** of their monthly income per operation, and companies up to **90%** of their monthly revenue.
- A withdrawal can never exceed the current balance.
- Money values are returned as strings (`"balance": "150.00"`) to preserve precision.

## Getting started

```bash
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
python run.py
```

The API runs at `http://localhost:5001`. Tables are created automatically on startup.

### Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `DATABASE_URL` | yes | SQLAlchemy connection string, e.g. `sqlite:///storage.db` |
| `FLASK_DEBUG` | no | `1` enables debug mode. Use only in development. |

In debug mode, unexpected errors reach the Flask debugger. Otherwise, they return a generic `500` response without internal details.

## Tests

```bash
pytest
```

The suite covers services, controllers, views, schemas, the database connection and the app factory. Tests use mocks between layers and an in-memory SQLite database, so no `.env` file is needed.

## Roadmap

Known improvements, planned but not yet done:

- **Integration tests** for every route using `app.test_client()`.
- **Remove duplication between client types.** `IndividualService` and `CompanyService`, and their repositories, differ only in configuration: client type, withdrawal ratio, not-found error, income field and table. The plan is to extract a `BaseClientService` and a `BaseClientRepository`, optionally using `__init_subclass__` to fail early when a subclass is missing configuration.
