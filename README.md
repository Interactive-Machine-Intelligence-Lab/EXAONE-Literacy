# 울산형 인공지능 리터러시 내용 체계 및 진단 도구

본 연구에서는 LG AI EXAONE을 기반으로 인공지능 리터러시 진단도구를 개발하고 있습니다.

<br>
<p align="center">
<img src="assets/EXAONE_Symbol+BI_3d.png", width="400", style="margin: 40 auto;">
<br>
<p align="center"> 🤗 <a href="https://huggingface.co/LGAI-EXAONE">HuggingFace</a> &nbsp | &nbsp 📝 <a href="https://www.lgresearch.ai/blog/view?seq=460"> Blog</a> &nbsp | &nbsp 📑 <a href="https://arxiv.org/abs/2408.03541"> Technical Report </a>
<br>

<br>

## 요구사항

- NVIDIA CUDA driver 지원이 가능한 GPU
- Anaconda 환경
- `transformers>=4.41.0`  (EXAONE 3.0 Model). 
- [streamlit](https://streamlit.io/) 환경 (웹 환경을 위함)

### secret

`secret/key.txt` 에 huggingface 토큰을 넣어주세요. 토큰은 레파지토리의 읽기 권한이 있어야만 합니다.


## Quickstart

```bash
 streamlit run app.py --server.fileWatcherType none
```

## Docker

`Dockerfile` 을 활용하여 도커파일을 통해 배포가 가능합니다. (8501 포트)
`scratch/`의 경우 `scratch-gui` 를 도커 파일을 통해 배포 중입니다.

# TODO

- 학생의 response, chatbot log DB에 저장하기
- 학생 별 고유 id를 통한 접근 가능하게 만들기
- scratch code를 web-view를 통해 visualize하기

### 문항

문항의 경우 중학교 이전 단원인 "알고리즘과 문제해결"을 참고하여 제작할 계획입니다.
중학교의 경우 직접 인공지능 모델의 동작원리의 이해보다는 전체적인 흐름-자료수집,라벨링,모델학습(자동화됨)-주기를 이해하는데 초점이 맞추어져 있습니다.
이에, 문제의 경우 주어진 scratch 형태의 코드를 AI를 통해 협력해서 수정하는 것을 목표로 삼습니다.
다만, 직접적으로 AI가 수정하는 것이 아닌 학생이 물음을 통해 AI가 수정하는 것으로 하고자 합니다. (바로 에러를 찾아내더군요.)