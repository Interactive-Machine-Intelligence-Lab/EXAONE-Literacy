from model import create_tables

def insert_mock_users(db):
    """
    사용자 Mock 데이터 삽입
    """
    mock_users = [
        ("UNIST", "BAE", "20211141"),
        ("UNIST", "KIM", "20210001"),
    ]

    for user in mock_users:
        query = "INSERT OR IGNORE INTO users (school_name, name, student_id) VALUES (?, ?, ?)"
        db.execute_query(query, user)

def insert_mock_problems(db):
    """
    문제 Mock 데이터 삽입
    """
    mock_problems = [
        (
            "팰린드롬 검사",
            """
            다음 코드는 스크래치 형태로 팰린드롬을 검사하는 코드입니다.
            팰린드롬은 앞으로 읽으나 뒤로 읽으나 같은 문자열을 말합니다.
            ```scratch
            when [space v] clicked
                set [userInput v] to [ask] and wait
                change background color by [10]
                ...
            ```
            """,
            1
        ),
        (
            "최소 동전 거스름돈",
            """
            다음 코드는 주어진 거스름돈에 대해 최소한의 동전 개수로 거슬러주는 코드입니다.
            ```python
            def min_coins(coins, amount):
                dp = [float('inf')] * (amount + 1)
                dp[0] = 0
                ...
            ```
            """,
            1
        ),
    ]

    for problem in mock_problems:
        query = "INSERT OR IGNORE INTO problems (title, description, credit) VALUES (?, ?, ?)"
        db.execute_query(query, problem)



# 실행 시 데이터베이스 초기화
if __name__ == "__main__":
    db = create_tables()
    insert_mock_problems(db)
    insert_mock_users(db)
    print("데이터베이스가 성공적으로 초기화되었습니다.")
