import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from .connection import DBConnectionHandler


@pytest.fixture(name="database_url")
def fixture_database_url(tmp_path):
    return f"sqlite:///{tmp_path / 'test.db'}"


def test_engine(database_url):
    db_connection_handler = DBConnectionHandler(database_url)

    assert db_connection_handler.get_engine() is None

    db_connection_handler.connect_to_db()

    db_engine = db_connection_handler.get_engine()

    assert db_engine is not None
    assert isinstance(db_engine, Engine)


def test_get_session_returns_new_session(database_url):
    db_connection_handler = DBConnectionHandler(database_url)

    db_connection_handler.connect_to_db()

    with db_connection_handler.get_session() as first_session:
        with db_connection_handler.get_session() as second_session:
            assert isinstance(first_session, Session)
            assert isinstance(second_session, Session)

            assert first_session is not second_session


def test_get_session_before_connect_to_db(database_url):
    db_connection_handler = DBConnectionHandler(database_url)

    with pytest.raises(RuntimeError):
        with db_connection_handler.get_session():
            pass


def test_get_session_propagates_exception(database_url):
    db_connection_handler = DBConnectionHandler(database_url)

    db_connection_handler.connect_to_db()

    with pytest.raises(ValueError):
        with db_connection_handler.get_session():
            raise ValueError
