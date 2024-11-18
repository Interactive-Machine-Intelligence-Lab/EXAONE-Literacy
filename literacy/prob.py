import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from literacy.chatbot import get_exaone_response, reset_chat_history

def problem(script: str='',
            prob_key: str='prob1'):
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
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(script)
        chatbot_textbox(prob_key)
    
    model.generation_config.pad_token_id = tokenizer.pad_token_id
    
    with col2:
        chatbot_chatbox(model, tokenizer)


def chatbot_textbox(prob_key: str='prob1'):
    if prob_key not in st.session_state:
        st.session_state[prob_key] = ""
    with st.form(key=prob_key+'box'):
        text_msg = "챗봇을 활용하여 주어진 주제에 맞는 글을 작성 후 `제출하기` 버튼을 눌러주세요.\n\n"
        text = st.text_area(text_msg, value=st.session_state[prob_key])
        submitted = st.form_submit_button("제출하기")
        if submitted:
            st.write("제출 완료: ", text)
            st.write("다음 단계로 이동합니다.")
            st.session_state[prob_key] = text
            st.rerun()
            
            
def chatbot_chatbox(model, tokenizer, 
                    script: str=''):
    st.info("EXAONE 모델을 사용한 챗봇입니다. 아래의 입력창에 질문을 입력하면 EXAONE 모델이 답변을 생성합니다.")
    # reset button
    st.button("채팅기록 초기화", on_click=reset_chat_history)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        reset_chat_history(script)

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        role = message["role"]
        if role == "system":
            continue
        with st.chat_message(role):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("입력을 넣어주세요."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # display the assistant response from stream
        with st.chat_message("assistant"):
            text_box = st.empty()
            for response in get_exaone_response(st.session_state.messages, model, tokenizer, script):
                text_box.markdown(response)
                
        print("챗봇 결과: ", response)
        st.session_state.messages.append({"role": "assistant", "content": response})