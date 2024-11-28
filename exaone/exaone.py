import streamlit as st

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread

def main():
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
    
    message_key = "messages"
    
    if message_key not in st.session_state:
        content = "You are EXAONE model from LG AI Research, a helpful assistant."
        st.session_state[message_key] = [{'role': 'system', 'content': content}]
    
    for message in st.session_state[message_key]:
        role = message["role"]
        if role == "system":
            continue
        with st.chat_message(role):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("입력을 넣어주세요."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state[message_key].append({"role": "user", "content": prompt})
        
        # display the assistant response from stream
        with st.chat_message("assistant"):
            text_box = st.empty()
            # parse input
            messages = []
            for message in st.session_state[message_key]:
                if message['content'] == '초기화 됨':
                    messages = []
                    continue
                messages.append(message)
            
            for response in get_exaone_response(messages, model, tokenizer):
                text_box.markdown(response)
                
        print("챗봇 결과: ", response)
        st.session_state[message_key].append({"role": "assistant", "content": response})

    

def get_exaone_response(messages,
                        model,
                        tokenizer,
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
        content = "You are EXAONE model from LG AI Research, a helpful assistant."
        messages = [{'role': 'system', 'content': content}]
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
    

if __name__ == '__main__':
    main()