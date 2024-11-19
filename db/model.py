import sqlite3

def create_tables():
    """
    테이블 구조 정의 및 생성
    """
    connection = sqlite3.connect("example.db")
    cursor = connection.cursor()

    # users 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER
    )
    """)
    connection.commit()
    connection.close()
