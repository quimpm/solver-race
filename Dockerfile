FROM python:3.8-alpine3.11
RUN mkdir /app
WORKDIR /app
RUN apk add pkgconfig graphviz graphviz-dev gcc musl-dev
COPY requirements.txt /app/
RUN python3 -m pip install pygraphviz --install-option="--library-path=/usr/lib/graphviz/"
RUN python3 -m pip install -r requirements.txt
COPY . /app
RUN python3 fracasat-graph-col.py out.png 2 1 3
