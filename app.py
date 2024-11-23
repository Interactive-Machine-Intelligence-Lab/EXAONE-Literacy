import copy 
import yaml

import streamlit as st
from literacy.prob import get_problem_page
from literacy.result import get_result_page


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
    
    for problem in problem_dict['problems']:
        name = problem['name']
        key = problem['key']
        problem_script = problem['script']
        url = problem['url']
        
        def prob_pg(script=problem_script, prob_key=key):
            return get_problem_page(script, prob_key)
        
        page_func = prob_pg
        # each page has its own session state
        page = st.Page(page_func, title=name, url_path=url)
        #page = st.Page(page_func, title=name, url_path=url, default=False)
        
        problem_pages.append(page)
        url_list.append(url)
    
    result = st.Page("literacy/result.py", title="Result")
    
    if 'authentication_status' in st.session_state and st.session_state.authentication_status:
        pg_dict = {
            "로그인": [login_page],
            "문제": problem_pages,
        } 
        
        result_list = []

        for url in url_list:
            if url in st.session_state:
                def result_pg(key=url):
                    return get_result_page(key)
                result = st.Page(result_pg, title=url+'_result', url_path=url+'_result')
                result_list.append(result)

        if result_list:
            pg_dict["결과"] = result_list
        pg = st.navigation(pg_dict)
    else:
        pg = st.navigation([login_page])
    pg.run()
    
    
