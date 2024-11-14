import streamlit as st


# FIXIT: 문제를 database화
sample_problem = r"""
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


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    
    login_page = st.Page("literacy/login.py", title="로그인")
    
    prob1 = st.Page("literacy/prob1.py", title="팰린드롬")
    result = st.Page("literacy/result.py", title="Result")

    if 'prob1' not in st.session_state:
        st.session_state['prob1'] = None
    if 'argument' not in st.session_state:
        st.session_state['argument'] = sample_problem
    
    if 'authentication_status' in st.session_state and st.session_state.authentication_status:
        pg_dict = {
            "계정": [login_page],
            "문제": [prob1],
        }
        if st.session_state.prob1 is not None:
            pg_dict["결과"] = result
        pg = st.navigation(pg_dict)
    else:
        pg = st.navigation([login_page])
    pg.run()
    
    
