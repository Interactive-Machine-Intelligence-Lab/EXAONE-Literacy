# app/Dockerfile

FROM node:lts-slim

# Set the working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g npm@latest
RUN git clone --depth=1 https://github.com/scratchfoundation/scratch-gui.git 

WORKDIR /app/scratch-gui
RUN npm install 
EXPOSE 8601 8601

ENTRYPOINT ["npm", "start"]