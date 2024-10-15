import streamlit as st


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    prob1 = st.Page("literacy/prob1.py", title="팰린드롬")

    if 'prob1' not in st.session_state:
        st.session_state['prob1'] = None
    if 'argument' not in st.session_state:
        # 팰린드롬 문제
        st.session_state['argument'] = r"""
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
    page_list = [prob1]
    
    if st.session_state.prob1 is not None:
        result = st.Page("literacy/result.py", title="Result")
        page_list.append(result)
    else:
        result = None
        
    pg = st.navigation(page_list)
    pg.run()