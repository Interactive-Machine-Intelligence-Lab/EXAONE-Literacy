import streamlit as st
import torch
from threading import Thread
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from db.controller import insert_rating

def get_result_page(title: str='',
                    script: str='',
                    key: str=''):
    # 문제
    st.title(title)
    st.write(script)
    
    # two columns layout
    col1, col2 = st.columns(2)
    
    text = st.session_state[key]
    
    with col1:
        st.markdown("## 문제 해결 결과")
        st.write("문제 해결 결과 내용")
        st.write(text)
        
        complete_time = st.session_state[key+'_time']
        # with min, second format
        minutes = complete_time // 60
        seconds = complete_time % 60
        seconds = round(seconds, 2)
        
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
    st.markdown("## 평가")
    st.markdown("### 문제해결능력")
    
    criteria = "다음과 같은 문제에 대한 답변을 수행했는지 여부를 평가하게 됩니다. 학생은 올바른 용어를 활용하여야 하며, 문제 내용 외의 질문을 해서는 안됩니다."
    criteria += "문제는 다음과 같습니다. "
    criteria += script
    with st.chat_message("assistant"):
        text_box = st.empty()
        for response in evaluate_script(criteria, text):
            text_box.write(response)
    
    st.markdown("### 비판적활용력")
    
    criteria = """다음과 같은 문제에 대한 답변을 수행했는지 여부를 평가하게 됩니다. 
    학생은 챗봇의 내용을 반복하는 것이 아닌, 비판적으로 수용하고 활용하여야 합니다.
    학생은 챗봇의 답변을 활용하여, 문제를 해결하는데 도움을 받아야 합니다.
    환각현상이 있을 시 이를 파악하고 되묻는 능력이 필요합니다."""
    criteria += "문제는 다음과 같습니다. "
    criteria += script
    criteria += "챗봇 로그는 다음과 같습니다."
    with st.chat_message("assistant"):
        text_box = st.empty()
        for response in evaluate_script(criteria, text, st.session_state[key + '_messages']):
            text_box.write(response)
            
    st.markdown("### 윤리적 활용능력")
    
    criteria = """다음과 같은 문제에 대한 답변을 수행했는지 여부를 평가하게 됩니다.
    학생은 챗봇의 답변을 윤리적으로 활용하여야 합니다.
    자신이 한 역할과 챗봇의 역할을 서술하여야 합니다."""
    criteria += "문제는 다음과 같습니다. "
    criteria += script
    criteria += "챗봇 로그는 다음과 같습니다."
    with st.chat_message("assistant"):
        text_box = st.empty()
        for response in evaluate_script(criteria, text, st.session_state[key + '_messages']):
            text_box.write(response)

    
        
def evaluate_script(criteria, input_text, logs=None):    
    model = model = AutoModelForCausalLM.from_pretrained(
            "LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct",
            cache_dir="models",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            device_map="auto",
        )
    tokenizer = AutoTokenizer.from_pretrained("LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct")
    
    content = "너는 LG AI Research의 EXAONE 모델이며, 도움이 되는 조력자입니다. "
    content += "따라오는 명령에 따라 답변을 수행해야만 합니다."
    content += "중학교 선생님으로써, 학생의 입력에 대해 평가를 수행하게 됩니다. 평가기준은 다음과 같습니다."
    content += "답변의 맨 앞에는 평가 결과가 우선되어야 하며, 평가는 매우 우수함, 우수함, 보통, 부족함, 매우 부족함으로 구성됩니다."
    content += "답변과 함께 학생을 지도할 때 사용할 수 있는 추가적인 정보를 제공해야 합니다."
    content += criteria
    
    messages = [{"role": "system", "content": content}]
    
    if logs:
        for log in logs:
            messages.append(log)
    
    messages.append({"role": "user", "content": "학생의 답변은 다음과 같습니다. 이를 평가하여야 합니다."})
    content = input_text
    
    messages.append({"role": "user", "content": content})
    
    tokens = tokenizer(content, return_tensors="pt").input_ids.to(model.device)
    
    streamer = TextIteratorStreamer(tokenizer, 
                                    timeout=60.0,
                                    skip_prompt=True,
                                    skip_special_tokens=True,)
    
    thread_kwargs = {
        "input_ids": tokens,
        "max_new_tokens": 2048,
        "do_sample": True,
        "top_p": 1.0,
        "top_k": 50,
        "temperature": 1.0,
        "streamer": streamer,
        "pad_token_id": 0,
        "eos_token_id": tokenizer.eos_token_id,
        }
    # parse output
    ## find the assistant response
    ## the assistant response is between "[|assistant|]" and "[|endofturn|]"
    # print the length of tokens
    
    with torch.no_grad():
        thread = Thread(target=model.generate, kwargs=thread_kwargs)
        thread.start()
        
    buffer = ""
    for new_text in streamer:
        buffer += new_text
        yield buffer