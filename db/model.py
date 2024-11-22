from db import Database

def create_tables():
    """
    테이블 구조 정의 및 생성
    """
    db = Database()

    # users 테이블 생성
    db.execute_query("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        school_name TEXT NOT NULL,
        name TEXT NOT NULL,
        student_id TEXT NOT NULL,
        score INTEGER DEFAULT null
    )
    """)

    # problems 테이블 생성
    db.execute_query("""
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        credit INTEGER DEFAULT null
    )
    """)

    db.execute_query("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        problem_id INTEGER NOT NULL,
        chat_log TEXT,
        result TEXT DEFAULT null,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    return db

# 실행
if __name__ == "__main__":
    db = create_tables()
    print("테이블이 성공적으로 생성되었습니다.")
