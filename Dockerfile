# app/Dockerfile

FROM continuumio/miniconda3:main

# Set the working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY models /app/models

# Copy the current directory contents into the container at /app
COPY requirements.yaml /app

RUN conda env create -f requirements.yaml

# activate the environment
RUN echo "conda activate $(head -1 /app/requirements.yaml | cut -d' ' -f2)" >> ~/.bashrc
ENV PATH=/opt/conda/envs/llm/bin:$PATH

COPY app.py /app
COPY literacy /app/literacy

COPY secret /app/secret
# environment variable from secret
RUN huggingface-cli login --add-to-git-credential --token $(cat /app/secret/key.txt) 

EXPOSE 8501 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
#ENTRYPOINT ["conda", "env", "list"]