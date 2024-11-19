import sqlite3

DB_NAME = "example.db"

class Database:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def connect(self):
        """
        데이터베이스에 연결
        """
        return sqlite3.connect(self.db_name)

    def execute_query(self, query, params=None):
        """
        쿼리 실행 (INSERT, UPDATE, DELETE)
        """
        connection = self.connect()
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        connection.close()

    def fetch_query(self, query, params=None):
        """
        쿼리 실행 (SELECT)
        """
        connection = self.connect()
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        return rows
