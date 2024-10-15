import streamlit as st

def visualize():
    # two columns layout
    col1, col2, col3 = st.columns(3)
    
    #with col1:
    #    st.markdown("## 챗봇 적용 이전 결과")
    #    st.markdown(st.session_state.step1)
        
    with col2:
        st.markdown("## 챗봇 적용 이후 결과")
        st.markdown(st.session_state.step2)
        
    with col3:
        # visualize the chatbot log
        st.markdown("## 챗봇 기록")
        for message in st.session_state.messages:
            role = message["role"]
            if role == "system":
                continue
            with st.chat_message(role):
                st.markdown(message["content"])
        
visualize()