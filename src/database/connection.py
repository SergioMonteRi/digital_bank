from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = "sqlite:///storage.db"
        self.__engine: Engine | None = None
        self.__session_maker = None

    def connect_to_db(self):
        self.__engine = create_engine(self.__connection_string)
        self.__session_maker = sessionmaker(bind=self.__engine, expire_on_commit=False)

    @contextmanager
    def get_session(self) -> Generator[Session]:
        if self.__session_maker is None:
            raise RuntimeError("Must call connect_to_db first")

        session = self.__session_maker()

        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_engine(self):
        return self.__engine


db_connection_handler = DBConnectionHandler()
