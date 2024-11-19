from db import Database

db = Database()

def insert_user(name, email, age):
    """
    사용자 추가
    """
    query = "INSERT INTO users (name, email, age) VALUES (?, ?, ?)"
    db.execute_query(query, (name, email, age))

def get_all_users():
    """
    모든 사용자 조회
    """
    query = "SELECT * FROM users"
    return db.fetch_query(query)

def get_user_by_email(email):
    """
    이메일로 사용자 조회
    """
    query = "SELECT * FROM users WHERE email = ?"
    return db.fetch_query(query, (email,))
