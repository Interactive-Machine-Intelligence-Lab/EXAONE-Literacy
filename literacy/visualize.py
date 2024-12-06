import regex as re
import yaml
import streamlit as st
import pandas as pd

from db.controller import get_school_users, get_answer_by_user_id
from literacy.result import get_result_page

DB_NAME = "ailit.db"

def get_problem():
    PATH = "./secret/problem.yaml"
    with open(PATH) as file:
        problem_dict = yaml.load(file, Loader=yaml.loader.SafeLoader)
    return problem_dict


def result_to_df(result, index):
    problem_dict = get_problem()
    
    for i in range(len(result)):
        problem_id = result[i][2]
        st.write('# '+ problem_dict['problems'][problem_id]['name'])
        complete_time = result[i][3]
        problem_solving = result[i][4]
        critical_thinking = result[i][5]
        ethical_utilization = result[i][6]
        data = {
            "시간": [complete_time],
            "문제해결능력": [problem_solving],
            "비판적활용력": [critical_thinking],
            "윤리적활용력": [ethical_utilization],   
        }
        
        minutes = int(complete_time // 60)
        seconds = complete_time % 60
        seconds = round(seconds, 2)
        
        if minutes == 0:
            complete_str = "{}초".format(seconds)
        else:
            complete_str = "{}분 {}초".format(minutes, seconds)
        
        for key, value in data.items():
            if key == "시간":
                st.write("걸린 시간: ", complete_str)
            else:
                st.write('## ' + key)
                st.write(value[0])
            #st.write(pd.DataFrame(data))
    if len(result) == 0:
        st.write("시험 데이터가 없습니다.")


def page_visualize():
    st.markdown("# 결과 시각화")
    problem_dict = get_problem()
    
    try:
        school_users = get_school_users(st.session_state["school_name"])
        school_user_names = [user[2] for user in school_users]
        
        school_user_name = st.selectbox("학생명", school_user_names)
        
        index = school_user_names.index(school_user_name)
        answers = get_answer_by_user_id(school_users[index][0])
        
        for answer in answers:
            problem_id = answer[2]
            chat_log = answer[3]
            chat_log = str_to_list(chat_log)
            
            student_answer = answer[4]
            
            st.session_state[problem_id] = student_answer
            st.session_state[problem_id + '_messages'] = chat_log
            
            for problem in problem_dict['problems']:
                problem_url = problem['url']
                problem_script = problem['script']
                problem_title = problem['name']
                if problem_url == problem_id:
                    script = problem_script
                    title = problem_title
                    
            get_result_page(title, script, problem_id)
            
            

    except Exception as e:
        # if list index out of range
        st.write("제출된 정보가 없습니다.")
        st.write(e)
    

def str_to_list(input_string):
    # I want to change from strings to list of dictionaries
    # example:
    # input_string = "[{'role': 'user', 'content': '안녕하세요'}, {'role': 'assistant', 'content': '안녕하세요!'}]"
    # output = [{'role': 'user', 'content': '안녕하세요'}, {'role': 'assistant', 'content': '안녕하세요!'}]
    
    # remove the first and last brackets
    input_string = input_string[2:-2]
    
    # split by '}, {' to get each dictionary
    input_string = input_string.split('}, {')
    # convert to list of dictionaries
    outputs = []
    for item in input_string:
        if type(item) == dict:
            pass
        # find 'role' and 'content' and add to the dictionary
        role = re.search(r"'role': '(.+?)'", item).group(1)
        content = re.search(r"'content': '(.+?)'", item).group(1)
        print(role, content)
        # add to the dictionary
        outputs.append({"role": role,
                        "content": content})
        
    return outputs
    
    


if __name__ == "__main__":
    page_visualize()