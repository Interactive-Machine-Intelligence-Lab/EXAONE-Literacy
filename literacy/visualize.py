import yaml
import streamlit as st
import pandas as pd

from db.controller import get_dataframe, get_school_users, get_rate_by_user_id

DB_NAME = "ailit.db"

#def dummy_data():
#    data = {
#        "학번": ['20210001', '20210002', '20210003', '20210004', '20210005'],
#        "학교": ['UNIST', 'UNIST', 'UNIST', '울산시', '울산시'],
#        "이름": ['김철수', '이영희', '박민수', '정미경', '홍길동'],
#        "시간": [10, 20, 30, 40, 50],
#        "개념이해도": [80, 70, 60, 50, 40],
#        "문제해결능력": [90, 80, 70, 60, 50],
#        "비판적활용력": [70, 60, 50, 40, 30],
#        "윤리적활용력": [60, 50, 40, 30, 20],
#    }
#    
#    return pd.DataFrame(data)

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
    
    try:
        school_users = get_school_users(st.session_state["school_name"])
        school_user_names = [user[2] for user in school_users]
        
        school_user_name = st.selectbox("학생명", school_user_names)
        
        index = school_user_names.index(school_user_name)

        rates = get_rate_by_user_id(school_users[index][0])
        result_to_df(rates, index)  

    except Exception as e:
        st.error(f"에러 발생: {e}")
    


if __name__ == "__main__":
    page_visualize()