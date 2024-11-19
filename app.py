import yaml

import streamlit as st
from literacy.prob import get_problem_page


def get_problem():
    PATH = "./secret/problem.yaml"
    with open(PATH) as file:
        problem_dict = yaml.load(file, Loader=yaml.loader.SafeLoader)
    return problem_dict

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    
    login_page = st.Page("literacy/login.py", title="로그인")
    
    problem_dict = get_problem()
    problem_pages = []
    url_list = []
    
    for problem in problem_dict['problems']:
        name = problem['name']
        script = problem['script']
        url = problem['url']
        
        page = st.Page(lambda: get_problem_page(script, url), title=name, url_path=url)
        
        problem_pages.append(page)
        url_list.append(url)
    
    print(url_list)
    result = st.Page("literacy/result.py", title="Result")
    
    if 'authentication_status' in st.session_state and st.session_state.authentication_status:
        pg_dict = {
            "문제": problem_pages,
        } 
        
        flag = True
        for url in url_list:
            if url in st.session_state:
                flag = False
                break
        if flag:
            pg_dict["결과"] = [result]
        pg = st.navigation(pg_dict)
    else:
        pg = st.navigation([login_page])
    pg.run()
    
    
