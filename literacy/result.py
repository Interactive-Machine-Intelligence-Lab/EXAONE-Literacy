import streamlit as st


def get_result_page(title: str='',
                    script: str='',
                    key: str=''):
    # 문제
    st.title(title)
    st.write('#'+title)
    st.write(script)
    
    # two columns layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 문제 해결 결과")
        st.write("문제 해결 결과 내용")
        st.write(st.session_state[key])
        st.write("걸린 시간: ", st.session_state[key+'_time'])
        
    with col2:
        st.markdown("## 챗봇 기록")
        for message in st.session_state[key + '_messages']:
            role = message["role"]
            if role == "system" and message["content"] != "초기화 됨":  
                continue
            with st.chat_message(role):
                st.markdown(message["content"])