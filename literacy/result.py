import streamlit as st

from db.controller import insert_rating

def get_result_page(title: str='',
                    script: str='',
                    key: str=''):
    # 문제
    st.title(title)
    st.write(script)
    
    # two columns layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 문제 해결 결과")
        st.write("문제 해결 결과 내용")
        st.write(st.session_state[key])
        
        print(st.session_state.to_dict().keys())
        
        complete_time = st.session_state[key+'_time']
        # with min, second format
        minutes = complete_time // 60
        seconds = complete_time % 60
        
        if minutes == 0:
            complete_str = "{}초".format(seconds)
        else:
            complete_str = "{}분 {}초".format(minutes, seconds)
        
        st.write("걸린 시간: ", complete_str)
        
    with col2:
        st.markdown("## 챗봇 기록")
        for message in st.session_state[key + '_messages']:
            role = message["role"]
            if role == "system" and message["content"] != "초기화 됨":  
                continue
            with st.chat_message(role):
                st.markdown(message["content"])
                
    # rating
    st.write("# 평가")
    st.write("아래의 슬라이더를 활용하여 문제해결 능력을 평가해주세요.")
    
    options = list(range(1, 6))
    
    understanding = st.select_slider("개념이해도", options, value=3)
    problem_solving = st.select_slider("문제해결능력", options, value=3)
    critical_thinking = st.select_slider("비판적사고능력", options, value=3)
    ethics = st.select_slider("윤리적 활용능력", options, value=3)
    
    if st.button("평가 제출"):
        st.write("평가가 제출되었습니다.")
        insert_rating(st.session_state['user_id'], key, understanding, problem_solving, critical_thinking, ethics)