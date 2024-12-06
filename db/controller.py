from db import Database


db = Database()


def get_rate_by_user_id(user_id):
    """
    사용자별 평가 조회
    """
    query = "SELECT * FROM ratings WHERE user_id = ?"
    return db.fetch_query(query, (user_id,))


def get_answer_by_user_id(user_id):
    """
    사용자별 답안 조회
    """
    query = "SELECT * FROM submissions WHERE user_id = ?"
    return db.fetch_query(query, (user_id,))


def get_school_users(school_name):
    """
    학교별 사용자 조회
    """
    query = "SELECT * FROM users WHERE school_name = ?"
    return db.fetch_query(query, (school_name,))


def get_dataframe():
    """
    데이터베이스에서 사용자 정보를 가져와서 DataFrame으로 반환
    """
    users = get_all_users()
    return users


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


def auth(school_name, name, student_id):
    print(f"Auth Input: {school_name}, {name}, {student_id}")
    
    # 입력 데이터 공백 제거
    school_name = school_name.strip()
    name = name.strip()
    student_id = str(student_id).strip()

    query = "SELECT * FROM users WHERE school_name = ? AND name = ? AND student_id = ?"
    result = db.fetch_query(query, (school_name, name, student_id))
    
    return {'status': len(result) > 0, 'id': 0 if len(result) == 0 else result[0][0]}


def insert_submission(user_id, problem_id, chat_log, result=None):
    """
    제출 내역 추가
    """
    # if query user_id and problem_id already exists, update the chat_log
    query = "SELECT * FROM submissions WHERE user_id = ? AND problem_id = ?"
    res = db.fetch_query(query, (user_id, problem_id))
    
    if len(res) > 0:
        query = "UPDATE submissions SET chat_log = ? WHERE user_id = ? AND problem_id = ?"
        db.execute_query(query, (str(chat_log), user_id, problem_id))
        return
    else:
        query = "INSERT INTO submissions (user_id, problem_id, chat_log, result) VALUES (?, ?, ?, ?)"
        db.execute_query(query, (user_id, problem_id, str(chat_log), result))
    
    
def insert_rating(user_id, problem_id, runtime, problem_solving, critical_thinking, ethics):
    """
    평가 추가
    """
    query = "SELECT * FROM ratings WHERE user_id = ? AND problem_id = ?"
    res = db.fetch_query(query, (user_id, problem_id))
    
    if len(res) > 0:
        query = "UPDATE ratings SET runtime = ?, problem_solving = ?, critical_thinking = ?, ethics = ? WHERE user_id = ? AND problem_id = ?"
        db.execute_query(query, (runtime, problem_solving, critical_thinking, ethics, user_id, problem_id))
        return
    else:
        query = "INSERT INTO ratings (user_id, problem_id, runtime, problem_solving, critical_thinking, ethics) VALUES (?, ?, ?, ?, ?, ?)"
        db.execute_query(query, (user_id, problem_id, runtime, problem_solving, critical_thinking, ethics))