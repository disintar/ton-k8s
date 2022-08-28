ARG  base
FROM ${base} AS builder

FROM python:3.10-bullseye AS git

RUN git clone https://github.com/toncenter/ton-http-api.git
WORKDIR ton-http-api
# latest commit in master
RUN git checkout 5d1717c
RUN rm -f ./pyTON/distlib/linux/libtonlibjson.so
COPY --from=builder /ton/build/tonlib/libtonlibjson.so.0.5 ./pyTON/distlib/linux/libtonlibjson.so

# fix /api/v2
RUN sed -i 's/\/api\/v2/\//g' ./pyTON/main.py

FROM python:3.10-slim

WORKDIR ton-http-api
COPY --from=git ton-http-api ./

RUN apt-get update && apt-get install -y gcc && \
  PIP_NO_CACHE_DIR=1 python3 -m pip install -r ./infrastructure/requirements/main.txt && \
  apt-get remove -y gcc && \
  apt-get autoremove -y && \
  apt-get install -y wget && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

ADD ./entrypoint.sh ./

ENTRYPOINT './entrypoint.sh'