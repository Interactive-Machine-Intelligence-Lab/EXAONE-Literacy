import streamlit as st
import pandas as pd

from db.controller import get_dataframe

DB_NAME = "ailit.db"

def dummy_data():
    data = {
        "학번": ['20210001', '20210002', '20210003', '20210004', '20210005'],
        "학교": ['UNIST', 'UNIST', 'UNIST', '울산시', '울산시'],
        "이름": ['김철수', '이영희', '박민수', '정미경', '홍길동'],
        "시간": [10, 20, 30, 40, 50],
        "개념이해도": [80, 70, 60, 50, 40],
        "문제해결능력": [90, 80, 70, 60, 50],
        "비판적활용력": [70, 60, 50, 40, 30],
        "윤리적활용력": [60, 50, 40, 30, 20],
    }
    
    return pd.DataFrame(data)


def page_visualize():
    st.markdown("# 결과 시각화")
    
    try:
        df = dummy_data()
        
        school_name = st.selectbox("학교명", df['학교'].unique())
        
        if not school_name:
            st.warning("학교를 선택해주세요.")
            return
        else:
            st.info(f"학교명: {school_name}")
            st.write(df[df['학교'] == school_name])
            
        df2 = get_dataframe()
        st.write(df2)
    except Exception as e:
        st.error(f"에러 발생: {e}")
    


if __name__ == "__main__":
    page_visualize()