import streamlit as st
import streamlit_authenticator as stauth
import yaml


def get_authenticators():
    # FIXIT: database에 ID/PW 저장
    with open("./secret/sample.yaml") as file: 
        config = yaml.load(file, Loader=yaml.loader.SafeLoader)
    
    print(__name__, config)
    
    authenticator = stauth.Authenticate(
        credentials=config['credentials'],
        cookie_name=config['cookie']['name'],
        cookie_key=config['cookie']['key'],
        cookie_expiry_days=config['cookie']['expiry_days'],
    )
    
    return authenticator


def page_login():
    authenticator = get_authenticators()
    
    authenticator.login('main')
    
    if st.session_state['authentication_status']:
        authenticator.logout('sidebar')
        st.write(f"환영합니다, {st.session_state['username'] }!")
        st.title("울산형 AI 리터러시")
    elif st.session_state['authentication_status'] == False:
        st.error("로그인에 실패했습니다.")
    elif st.session_state['authentication_status'] == None:
        st.warning("username과 password를 입력해주세요.")
        
page_login()