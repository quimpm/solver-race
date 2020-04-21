FROM python:3.8-alpine3.11
RUN mkdir /app
WORKDIR /app
RUN apk add pkgconfig graphviz graphviz-dev gcc musl-dev
COPY requirements.txt /app/
RUN python3 -m pip install pygraphviz --install-option="--library-path=/usr/lib/graphviz/"
COPY . /app
RUN python3 fracaSAT.py ex-graph1.cnf