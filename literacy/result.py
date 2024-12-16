import streamlit as st
import torch
from threading import Thread
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from db.controller import insert_rating

from literacy.chatbot import get_exaone_response

def get_result_page(title: str='',
                    script: str='',
                    key: str=''):
    # 문제
    st.title(title)
    st.write(script)
    
    # load the model
    @st.cache_resource  
    def load_model():
        # To avoid downloading new versions of the code file, you can pin a revision.
        model = AutoModelForCausalLM.from_pretrained(
            "LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct",
            cache_dir="models",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            device_map="auto",
        )
        return model
    
    @st.cache_resource
    def get_tokenizer():
        return AutoTokenizer.from_pretrained("LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct")
    
    model = load_model()
    tokenizer = get_tokenizer()
    
    # two columns layout
    col1, col2 = st.columns(2)
    
    text = st.session_state[key]
    
    with col1:
        st.markdown("## 문제 해결 결과")
        st.write("문제 해결 결과 내용")
        st.write(text)
        
    with col2:
        st.markdown("## 챗봇 기록")
        for message in st.session_state[key + '_messages']:
            role = message["role"]
            if role == "system" and message["content"] != "초기화 됨":  
                continue
            with st.chat_message(role):
                st.markdown(message["content"])
                
    # rating
    st.markdown("## 평가")
    st.markdown("### 문제해결능력")
    response_list = []
    
    init_content = "You are EXAONE model from LG AI Research, a helpful assistant."
    init_content += """You assistant following the conversation and provide helpful responses. 
        You are teacher of the middle school. """
    messages = [{"role": "system", "content": init_content}]
    
    content = """다음과 같은 문제에 대한 답변을 수행했는지 여부를 json 형태로 출력하세요. 
    학생은 올바른 용어를 활용하여야 하며, 문제 내용 외의 질문을 해서는 안됩니다.
    학생의 답변에 대한 점수는 1~5점까지 부여됩니다. 이후 장점과 단점, 그리고 교육적 활용방안에 대해 작성하세요.
    """
    content += "문제는 다음과 같습니다. "
    content += script
    content += "학생의 답변은 다음과 같습니다"
    content += text
    messages.append({"role": "user", "content": content})
    
    with st.chat_message("assistant"):
        text_box = st.empty()
        for response in get_exaone_response(messages, model, tokenizer):
            text_box.write(response)
        response_list.append(response)

    st.markdown("### 비판적 활용능력")
    
    messages = [{"role": "system", "content": init_content}]
    
    criteria = """ 학생이 챗봇의 결과를 비판적으로 수용할 수 있는지 여부를 json 형태로 출력하세요.
    학생은 챗봇의 내용을 반복하는 것이 아닌, 비판적으로 수용하고 활용하여야 합니다.
    학생은 챗봇의 답변을 활용하여, 문제를 해결하는데 도움을 받아야 합니다.
    환각현상이 있을 시 이를 파악하고 되묻는 능력이 필요합니다."""
    criteria += "문제는 다음과 같습니다. "
    criteria += script
    criteria += "챗봇 로그는 다음과 같습니다."
    messages.append({"role": "user", "content": criteria})
    for message in st.session_state[key + '_messages']:
        role = message["role"]
        if role == "system" and message["content"] != "초기화 됨":  
            continue
        messages.append(message)
    
    message = """
    다음과 같은 문제에 대한 비판적으로 수행했는지 여부를 json 형태로 출력하세요. 
    학생의 답변에 대한 점수는 1~5점까지 부여됩니다. 이후 장점과 단점, 그리고 교육적 활용방안에 대해 작성하세요.
    """
    messages.append({"role": "user", "content": message})

    with st.chat_message("assistant"):
        text_box = st.empty()
        for response in get_exaone_response(messages, model, tokenizer):
            text_box.write(response)
        response_list.append(response)
            
    st.markdown("### 윤리적 활용능력")
    
    criteria = """다음과 같은 문제에 대한 답변을 수행했는지 여부를 평가하게 됩니다.
    학생은 챗봇의 답변을 윤리적으로 활용하여야 합니다.
    자신이 한 역할과 챗봇의 역할을 서술하여야 합니다."""
    criteria += "문제는 다음과 같습니다. "
    criteria += script
    criteria += "챗봇 로그는 다음과 같습니다."
    messages = [{"role": "user", "content": criteria}]
    
    for message in st.session_state[key + '_messages']:
        role = message["role"]
        if role == "system" and message["content"] != "초기화 됨":  
            continue
        messages.append(message)
    
    message = "학생이 윤리적으로 챗봇의 답변을 활용하였는지 여부를 json 형태로 출력하세요. 학생의 답변에 대한 점수는 1~5점까지 부여됩니다."
    messages.append({"role": "user", "content": message})
    
    with st.chat_message("assistant"):
        text_box = st.empty()
        for response in get_exaone_response(messages, model, tokenizer):
            text_box.write(response)
        response_list.append(response)

    convert_dict = {
        'change': 1,
        'temperature': 2,
        'palindrome': 3,
    }

    insert_rating(
        user_id=st.session_state['user_id'],
        problem_id=convert_dict[key],
        runtime=0,
        problem_solving=response_list[0],
        critical_thinking=response_list[1],
        ethics=response_list[2],
    )