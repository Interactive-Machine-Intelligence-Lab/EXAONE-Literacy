import streamlit as st


# FIXIT: 문제를 database화


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    
    login_page = st.Page("literacy/login.py", title="로그인")
    
    prob1 = st.Page("literacy/prob1.py", title="팰린드롬")
    prob2 = st.Page("literacy/prob2.py", title="팰린드롬2")
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
    
    
