import streamlit as st
from literacy.prob import problem


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    
    login_page = st.Page("literacy/login.py", title="로그인")
    
    #prob1 = st.Page("literacy/prob1.py", title="팰린드롬")
    prob1 = st.Page(lambda: problem(sample_problem1, 'prob1'), title="팰린드롬")
    prob2 = st.Page(lambda: problem(sample_problem2, 'prob2'), title="거스름돈")
    
    result = st.Page("literacy/result.py", title="Result")
    
    if 'authentication_status' in st.session_state and st.session_state.authentication_status:
        pg_dict = {
            "문제": [prob1, prob2],
        }
        if 'prob1' in st.session_state and 'prob2' in st.session_state:
            pg_dict["결과"] = [result]
        pg = st.navigation(pg_dict)
    else:
        pg = st.navigation([login_page])
    pg.run()
    
    
# FIXIT: 문제를 database화
sample_problem1 = r"""
            다음 코드는 스크래치 형태로 팰린드롬을 검사하는 코드입니다.
            팰린드롬은 앞으로 읽으나 뒤로 읽으나 같은 문자열을 말합니다.
            ```scratch
            // Scratch로 작성된 팰린드롬 검사 프로그램

            when [space v] clicked
                set [userInput v] to [ask] and wait
                change background color by [10]

                // 사용자 입력을 소문자로 변환
                set [input lower v] to (lowerletters (userInput))

                // 길이 체크
                if <(length of) (input lower v) < 2> then
                    say [This text is too short to be a word.] for (1) seconds
                    broadcast [OK]

                repeat (length of) (input lower v)
                    if <not ((input lower v) at (index)) = ((input lower v) at ((index) + (1)))> then
                        broadcast [This text is not a palindrome.]
                        broadcast [OK]
                        stop

                broadcast [This text is a palindrome.]
                broadcast [OK]
            end
            ```
            """

sample_problem2 = r"""
            다음 코드는 주어진 거스름돈에 대해 최소한의 동전 개수로 거슬러주는 코드입니다.
            ```python
            def min_coins
            ```
            """
            