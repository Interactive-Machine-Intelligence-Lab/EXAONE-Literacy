import re

import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

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
        st.session_state.messages = [{"role": "system", 
            "content": "You are EXAONE model from LG AI Research, a helpful assistant."}]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("입력을 넣어주세요."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        response = get_exaone(st.session_state.messages, model,tokenizer)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        #memory.chat_memory.add_ai_message(response)

def get_exaone(messages,
               model,
               tokenizer,
               max_length=4096,
               chunk_size=1024):
    tokens = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        )
    print("len", tokens.shape)
    outputs = []
    for i in range(0, len(tokens), chunk_size):
        chunk = tokens[:,i:i+chunk_size]
        
        with torch.no_grad():
            output_chunk = model.generate(chunk.to("cuda"), 
                                          max_new_tokens=max_length,
                                          pad_token_id=tokenizer.eos_token_id)
        outputs.append(output_chunk)
    final_output = torch.cat(outputs, dim=0)
    print("final_output", final_output.shape)
    output = tokenizer.decode(final_output[0])
    # parse output
    ## find the assistant response
    ## the assistant response is between "[|assistant|]" and "[|endofturn|]"
    responses = re.findall(r"\[\|assistant\|\](.*?)\[\|endofturn\|\]", output, re.DOTALL)
    if responses:
        # remove empty string
        responses = [response for response in responses if response]
    response = responses[-1] if responses else output
    return response
  
if __name__ == "__main__":
    main()
