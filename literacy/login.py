import streamlit as st
from db.controller import auth, get_all_users

def page_login():
    """
    사용자 로그인 페이지
    """
    # 로그인 입력 필드
    st.title("로그인")
    school_name = st.text_input("학교명", key="school_name")
    name = st.text_input("이름", key="name")
    student_id = st.text_input("학생 번호", key="student_id")

    if st.button("로그인"):
        # 데이터베이스를 통해 인증 처리
        res = auth(school_name, name, student_id)
        if res["status"]:
            st.success(f"환영합니다, {name}!")
            st.session_state['authentication_status'] = True
            st.session_state['username'] = name
            st.session_state["user_id"] = res["id"]
            st.rerun()
        else:
            st.error("로그인에 실패했습니다. 정보를 확인하세요.")

    # 로그아웃 처리
    if st.session_state.get('authentication_status'):
        if st.button("로그아웃"):
            st.session_state['authentication_status'] = False
            st.session_state['username'] = None
            st.success("성공적으로 로그아웃되었습니다.")
            st.rerun()
        
page_login()