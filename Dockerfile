FROM python:3.7-slim-buster

RUN apt-get update \
        && apt-get install -y build-essential build-essential python3.7-dev python-igraph

COPY . /pimbook
WORKDIR "/pimbook"

RUN pip3 install -r requirements.txt

ENTRYPOINT ["bash"]
