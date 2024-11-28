import copy 
import yaml

import streamlit as st
from literacy.prob import get_problem_page
from literacy.result import get_result_page
from literacy.visualize import page_visualize


def get_problem():
    PATH = "./secret/problem.yaml"
    with open(PATH) as file:
        problem_dict = yaml.load(file, Loader=yaml.loader.SafeLoader)
    return problem_dict
    


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    
    login_page = st.Page("literacy/login.py", title="로그인", default=True)
    
    problem_dict = get_problem()
    
    problem_pages = []
    url_list = []

    manage_pages = []

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
    
    if 'authentication_status' in st.session_state and st.session_state.authentication_status:
        if st.session_state.get('manager'):
            pg_dict = {
                "로그인": [login_page],
                "문제": problem_pages,
                "관리자 페이지": manage_pages
            }
        else:
            pg_dict = {
                "로그인": [login_page],
                "문제": problem_pages
            }
        
        result_list = []

        for url in url_list:
            if url + '_time' in st.session_state:
                # find the script with the match url
                for problem in problem_dict['problems']:
                    if problem['url'] == url:
                        title = problem['name']
                        script = problem['script']
                        break
                def result_pg(title=title, script=script, key=url):
                    return get_result_page(title, script, key)
                result = st.Page(result_pg, title=url+'_result', url_path=url+'_result')
                result_list.append(result)

        if result_list:
            pg_dict["결과"] = result_list
        pg = st.navigation(pg_dict)
    else:
        pg = st.navigation([login_page])
    pg.run()
    
    
