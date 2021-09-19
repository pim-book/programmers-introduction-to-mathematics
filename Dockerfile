FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
COPY install.sh install.sh

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev bash

RUN sh ./install.sh

COPY . .

