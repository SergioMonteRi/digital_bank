import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from .connection import DBConnectionHandler


def test_engine():
    db_connection_handler = DBConnectionHandler()

    assert db_connection_handler.get_engine() is None

    db_connection_handler.connect_to_db()

    db_engine = db_connection_handler.get_engine()

    assert db_engine is not None
    assert isinstance(db_engine, Engine)


def test_get_session_returns_new_session():
    db_connection_handler = DBConnectionHandler()

    db_connection_handler.connect_to_db()

    with db_connection_handler.get_session() as first_session:
        with db_connection_handler.get_session() as second_session:
            assert isinstance(first_session, Session)
            assert isinstance(second_session, Session)

            assert first_session is not second_session


def test_get_session_before_connect_to_db():
    db_connection_handler = DBConnectionHandler()

    with pytest.raises(RuntimeError):
        with db_connection_handler.get_session():
            pass


def test_get_session_propagates_exception():
    db_connection_handler = DBConnectionHandler()

    db_connection_handler.connect_to_db()

    with pytest.raises(ValueError):
        with db_connection_handler.get_session():
            raise ValueError
