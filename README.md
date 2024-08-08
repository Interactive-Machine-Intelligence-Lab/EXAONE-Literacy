# EXAONE 3.0
<br>
<p align="center">
<img src="assets/EXAONE_Symbol+BI_3d.png", width="400", style="margin: 40 auto;">
<br>
<p align="center"> 🤗 <a href="https://huggingface.co/LGAI-EXAONE">HuggingFace</a> &nbsp | &nbsp 📝 <a href="https://www.lgresearch.ai/blog/view?seq=460"> Blog</a> &nbsp | &nbsp 📑 <a href="https://arxiv.org/abs/2408.03541"> Technical Report </a>
<br>

<br>

## Introduction

We introduce EXAONE-3.0-7.8B-Instruct, a pre-trained and instruction-tuned bilingual (English and Korean) generative model with 7.8 billion parameters. 
The model was pre-trained with 8T curated tokens and post-trained with supervised fine-tuning and direct preference optimization. 
It demonstrates highly competitive benchmark performance against other state-of-the-art open models of similar size. 

<br>

## News

- 2024.08.07: We released the EXAONE 3.0 7.8B instruction-tuned model. Check out the 📑 [Technical Report](https://arxiv.org/abs/2408.03541)!

<br>

## Performance

Some experimental results are shown below. The full evaluation results can be found in the [Technical Report](https://arxiv.org/abs/2408.03541).

| Language | Benchmark | EXAONE 3.0 <br>7.8B Inst. | Llama 3.1 <br>8B Inst. | Gemma 2 <br>9B Inst. | QWEN 2 <br>7B Inst. | Phi 3 <br>7B Inst. | Mistral 7B <br>Inst. |
| :-----: | :----- | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: |
| English | MT-Bench          | **9.01** | 7.95 | 8.52 | 8.41 | 8.52 | 7.72 |
|         | Arena-Hard-v0.1   | **46.8** | 28.0 | 42.1 | 21.7 | 29.1 | 16.2 |
|         | WildBench         | **48.2** | 34.5 | 41.5 | 34.9 | 32.8 | 29.0 |
|         | AlpacaEval 2.0 LC | 45.0 | 31.5 | **47.5** | 24.5 | 37.1 | 31.0 |
| Korean  | KoMT-Bench[^1]    | **8.92** | 6.06 | 7.92 | 7.69 | 4.87 | 5.20 |
|         | LogicKor          | **8.62** | 5.40 | 8.07 | 6.12 | 3.76 | 3.42 |

<br>

## Requirements

- `transformers>=4.41.0` for the EXAONE 3.0 Model. The Latest version is recommended to use.

<br>

## Quickstart

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct",
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct")

# Choose your prompt
prompt = "Explain who you are"  # English example
prompt = "너의 소원을 말해봐"   # Korean example

messages = [
    {"role": "system", "content": "You are EXAONE model from LG AI Research, a helpful assistant."},
    {"role": "user", "content": prompt}
]
input_ids = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt"
)

output = model.generate(
    input_ids.to("cuda"),
    eos_token_id=tokenizer.eos_token_id,
    max_new_tokens=128
)
print(tokenizer.decode(output[0]))
```

> [!Note]
> The EXAONE 3.0 instruction-tuned language model was trained to utilize the system prompt, 
> so we highly recommend using the system prompts provided in the code snippet above.

<br>

## Limitation

The EXAONE language model has certain limitations and may occasionally generate inappropriate responses. The language model generates responses based on the output probability of tokens, and it is determined during learning from training data. While we have made every effort to exclude personal, harmful, and biased information from the training data, some problematic content may still be included, potentially leading to undesirable responses. Please note that the text generated by EXAONE language model does not reflects the views of LG AI Research.

- Inappropriate answers may be generated, which contain personal, harmful or other inappropriate information.
- Biased responses may be generated, which are associated with age, gender, race, and so on.
- The generated responses rely heavily on statistics from the training data, which can result in the generation of
semantically or syntactically incorrect sentences.
- Since the model does not reflect the latest information, the responses may be false or contradictory.

LG AI Research strives to reduce potential risks that may arise from EXAONE language model. Users are not allowed
to engage in any malicious activities (e.g., keying in illegal information) that may induce the creation of inappropriate
outputs violating LG AI’s ethical principles when using EXAONE language model.

<br>

## License

The model is licensed under [EXAONE AI Model License Agreement 1.0 - NC](./LICENSE)
 
<br>
 
## Citation
 
```
@article{exaone-3.0-7.8B-instruct,
  title={EXAONE 3.0 7.8B Instruction Tuned Language Model},
  author={LG AI Research},
  journal={arXiv preprint arXiv:2408.03541},
  year={2024}
}
```

<br>

## Contact
LG AI Research Technical Support: contact_us@lgresearch.ai

[^1]: KoMT-Bench is a dataset created by translating MT-Bench into Korean; see [README](https://github.com/LG-AI-EXAONE/KoMT-Bench) for more details.