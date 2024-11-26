from threading import Thread

import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

def get_exaone_response(messages,
                        model,
                        tokenizer,
                        script='',
                        key='prob1',
                        max_length=2048,
                        chunk_size=1024,
                        device='cuda'):
    
    tokens = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        ).to(device)
    
    # note that the maximum length of the model is 4096s
    if tokens.shape[1] > max_length:
        warn_msg = "입력이 가능한 최대 길이를 초과했습니다. 채팅 로그가 초기화됩니다.".format(max_length, tokens.shape[1], max_length)
        st.warning(warn_msg)
        reset_chat_history(script, key)
    else:
        info_msg = "입력이 가능한 최대 길이는 {} 토큰 입니다. 현재 {} 토큰이 사용되었습니다.".format(max_length, tokens.shape[1])
        st.info(info_msg)
    
    streamer = TextIteratorStreamer(tokenizer, 
                                    timeout=60.0,
                                    skip_prompt=True,
                                    skip_special_tokens=True,)
    
    thread_kwargs = {
        "input_ids": tokens,
        "max_new_tokens": max_length,
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
        
        
def reset_chat_history(script: str='', 
                       key: str='prob1'):
    content = "You are EXAONE model from LG AI Research, a helpful assistant."
    content += """You assistant following the conversation and provide helpful responses. 
        You are teacher of the middle school. 
        However, you must not directly find the error. 
        Also, you must not directly show the fixed code. 
        You must not write the whole code for the user.
        You must not write python code.
        You only allow to debug when the error is found by user."""
    content += script
    
    key_messages = key + '_messages'
    
    if key_messages not in st.session_state:
        st.session_state[key_messages] = []
    else:
        st.session_state[key_messages].append({"role": "system", "content": '초기화 됨'})
    
    st.session_state[key_messages].append({"role": "system", "content": content})
