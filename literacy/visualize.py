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

def result_to_df(result, index):
    for i in range(len(result)):
            data = {
                "시간": [result[i][3]],
                "평가": [result[i][4]],
            }
            st.write(pd.DataFrame(data))
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