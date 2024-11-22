import streamlit as st

def visualize(key_list  = ["prob1", "prob2", "messages"]):
    # two columns layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # visualize the step1
        st.markdown("## Step1")
        st.write("Step1 내용")
        st.write(st.session_state[key_list[0]])
        
    with col2:
        # visualize the step2
        st.markdown("## Step2")
        st.write("Step2 내용")
        st.write(st.session_state[key_list[1]])
        
    with col3:
        # visualize the chatbot log
        st.markdown("## 챗봇 기록")
        for message in st.session_state.messages:
            role = message["role"]
            if role == "system":
                continue
            with st.chat_message(role):
                st.markdown(message["content"])
        

def get_result_page(key: str=''):
    # two columns layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 문제 해결 결과")
        st.write("문제 해결 결과 내용")
        st.write(st.session_state[key])
        
    with col2:
        st.markdown("## 챗봇 기록")
        for message in st.session_state[key + '_messages']:
            role = message["role"]
            if role == "system" and message["content"] != "초기화 됨":  
                continue
            with st.chat_message(role):
                st.markdown(message["content"])