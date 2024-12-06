import regex as re
import yaml
import streamlit as st
import pandas as pd

from db.controller import get_school_users, get_answer_by_user_id

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
            
            print(problem_id)
            print(chat_log)
            print(student_answer)

    except Exception as e:
        # if list index out of range
        st.write("제출된 정보가 없습니다.")
        st.write(e)
    

def str_to_list(inputs):
    # I want to change from strings to list of dictionaries
    # example:
    # inputs = "[{'role': 'user', 'content': '안녕하세요'}, {'role': 'assistant', 'content': '안녕하세요!'}]"
    # output = [{'role': 'user', 'content': '안녕하세요'}, {'role': 'assistant', 'content': '안녕하세요!'}]
    
    # remove the first and last brackets
    inputs = inputs[2:-2]
    
    # split by '}, {' to get each dictionary
    inputs = inputs.split('}, {')
    # convert to list of dictionaries
    print("inputs: ", inputs)   
    
    return inputs
    
    


if __name__ == "__main__":
    page_visualize()