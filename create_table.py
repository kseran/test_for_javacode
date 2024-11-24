from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import Base


class TableManage:
    def __init__(self):
        self._DB_USER = 'postgres'
        self._DB_PASSWORD = '34345656q'
        self._DB_HOST = 'localhost'
        self._DB_PORT = '5432'
        self._DB_NAME = 'test_for_javacode_db'

    def created_engine(self):
        database_url = f'postgresql://{self._DB_USER}:{self._DB_PASSWORD}@{self._DB_HOST}:{self._DB_PORT}/{self._DB_NAME}'
        engine = create_engine(database_url)
        return engine

    def created_session(self):
        return sessionmaker(bind=self.created_engine())

    def check_table(self):
        table_names = ['wallet']
        inspector = inspect(self.created_engine())

        for table_name in table_names:
            if not inspector.has_table(table_name):
                Base.metadata.create_all(TableManage().created_engine())
                break


if __name__ == "__main__":
    Base.metadata.create_all(TableManage().created_engine())
