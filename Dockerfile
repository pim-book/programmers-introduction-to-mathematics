FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
COPY install.sh install.sh

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
RUN apk add jpeg-dev zlib-dev libjpeg make bash
RUN apk add gfortran py-pip build-base wget freetype-dev libpng-dev openblas-dev

RUN sh ./install.sh

COPY . .

