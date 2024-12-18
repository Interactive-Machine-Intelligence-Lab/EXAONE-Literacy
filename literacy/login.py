import streamlit as st


def logout():
    if st.button("로그아웃"):
        st.session_state.authentication_status = False
        st.session_state['username'] = None
        st.rerun()
        
        
if __name__ == "__main__":
    logout()