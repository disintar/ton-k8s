ARG  base
FROM ${base} as builder

FROM python:3.10-slim-bullseye

COPY --from=builder /ton/build/blockchain-explorer/blockchain-explorer /usr/local/bin/
COPY ./start.sh /


RUN apt-get update && apt-get install -y libsecp256k1-dev libsodium-dev libmicrohttpd12 wget && apt-mark manual libmicrohttpd12 wget &&\
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN ln -s /lib/x86_64-linux-gnu/libsecp256k1.so.1.0.0 /usr/lib/libsecp256k1.so.0

ENTRYPOINT ["/start.sh"]
