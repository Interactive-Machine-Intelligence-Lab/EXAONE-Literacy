import copy 
import yaml

import streamlit as st

from db.controller import auth, get_all_users
from literacy.prob import get_problem_page
from literacy.result import get_result_page
from literacy.visualize import page_visualize
from literacy.login import logout


def get_problem():
    PATH = "./secret/problem.yaml"
    with open(PATH) as file:
        problem_dict = yaml.load(file, Loader=yaml.loader.SafeLoader)
    return problem_dict


def page_login():
    """
    사용자 로그인 페이지
    """
    if 'school_name' not in st.session_state:
        st.session_state['school_name'] = ''
    # 로그인 입력 필드
    #st.title("로그인 페이지")
    school_name = st.text_input("학교명", key="school")
    name = st.text_input("이름", key="name")
    student_id = st.text_input("학생 번호", key="student_id")

    if 'manager' not in st.session_state:
        st.session_state["manager"] = False

    if st.button("로그인"):
        # 데이터베이스를 통해 인증 처리
        res = auth(school_name, name, student_id)
        if res["status"]:
            st.success(f"환영합니다, {name}!")
            st.session_state['authentication_status'] = True
            st.session_state['username'] = name
            st.session_state["user_id"] = res["id"]
            st.session_state["school_name"] = school_name
            
            if 'T' in student_id:
                st.session_state["manager"] = True
            #print("IN FUNC", st.session_state)
            st.rerun()
        else:
            st.error("로그인에 실패했습니다. 정보를 확인하세요.")


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("울산형 AI 리터러시 진단도구")
    
    problem_dict = get_problem()
    
    problem_pages = []
    url_list = []

    manage_pages = []
    
    print(st.session_state)
    
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = False

    if st.session_state.get('manager'):
        def manage_pg():
            return page_visualize()

        page_func = manage_pg
        page = st.Page(page_func, title="학생 점수 관리", url_path='manage')

        manage_pages.append(page)
    
    for problem in problem_dict['problems']:
        name = problem['name']
        key = problem['key']
        problem_script = problem['script']
        url = problem['url']
        
        def prob_pg(script=problem_script, prob_key=url):
            return get_problem_page(script, prob_key)
        
        page_func = prob_pg
        # each page has its own session state
        page = st.Page(page_func, title=name, url_path=url)
        #page = st.Page(page_func, title=name, url_path=url, default=False)
        
        problem_pages.append(page)
        url_list.append(url)
    
    
    if st.session_state.authentication_status:
        logout_page = st.Page(logout, title="로그아웃", icon=":material/logout:")
        if st.session_state.get('manager'):
            pg_dict = {
                "계정 관리": [logout_page],
                "관리자 페이지": manage_pages
            }
        else:
            pg_dict = {
                "계정 관리": [logout_page],
                "문제": problem_pages
            }
        
        result_list = []

        pg = st.navigation(pg_dict)
    else:
        print("not authenticated", st.session_state)
        pg = st.navigation([st.Page(page_login)])
        
    pg.run()
    
    
