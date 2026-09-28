from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = "sqlite:///storage.db"
        self.__engine: Engine | None = None
        self.__session: Session | None = None

    def connect_to_db(self):
        self.__engine = create_engine(self.__connection_string)

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_maker = sessionmaker(bind=self.__engine)
        self.__session = session_maker()

        return self.__session

    def __exit__(self, exc_type, exc, tb):
        if self.__session:
            self.__session.close()


db_connection_handler = DBConnectionHandler()
