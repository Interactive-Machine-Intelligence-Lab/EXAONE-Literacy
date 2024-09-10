import re
from threading import Thread

import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer


def main():
    st.title("Exaone Bot")
    
    # load the model
    @st.cache_resource  
    def load_model():
        model = AutoModelForCausalLM.from_pretrained(
            "LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            device_map="auto"
        )
        return model
    
    @st.cache_resource
    def get_tokenizer():
        return AutoTokenizer.from_pretrained("LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct")
    
    model  = load_model()
    tokenizer = get_tokenizer()
    
    model.generation_config.pad_token_id = tokenizer.pad_token_id

    # Initialize chat history
    if "messages" not in st.session_state:
        ## Init chat history 
        st.session_state.messages = [{"role": "system", 
            "content": "You are EXAONE model from LG AI Research, a helpful assistant."}]

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
            for response in get_exaone(st.session_state.messages, model,tokenizer):
                text_box.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

def get_exaone(messages,
               model,
               tokenizer,
               max_length=4096,
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
        warn_msg = "입력이 가능한 최대 길이를 초과했습니다. 최대 길이는 {} 토큰 입니다. 현재 {} 토큰이 사용되었으며, 최근 {} 토큰만큼 사용합니다.".format(max_length, tokens.shape[1], max_length)
        st.warning(warn_msg)
        tokens = tokens[:, -max_length:]
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
    print(tokens.shape)
    
    with torch.no_grad():
        thread = Thread(target=model.generate, kwargs=thread_kwargs)
        thread.start()
        
    buffer = ""
    for new_text in streamer:
        buffer += new_text
        yield buffer
  
if __name__ == "__main__":
    main()
