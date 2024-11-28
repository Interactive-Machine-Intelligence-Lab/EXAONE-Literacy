import streamlit as st
import torch
from threading import Thread

def get_manage_page(title: str='',
                    script: str='',
                    key: str=''):
    st.title(title)
    st.write(script)

    st.markdown("## 학생 점수 조회 및 관리")
    st.write("학생 점수 조회")