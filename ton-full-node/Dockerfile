ARG  base
FROM ${base} as builder

FROM python:3.10-slim-bullseye

RUN mkdir -p /var/ton-work/db/static
RUN mkdir -p /var/ton-work/db/dht-server

ENV FIFTPATH /usr/local/lib/fift

COPY --from=builder \
  /ton/build/lite-client/lite-client \
  /ton/build/validator-engine/validator-engine \
  /ton/build/validator-engine-console/validator-engine-console \
  /ton/build/utils/generate-random-id \
  /ton/build/blockchain-explorer/blockchain-explorer \
  /ton/build/test-ton-collator \
  /ton/build/crypto/fift \
  /ton/build/crypto/func \
  /ton/build/dht-server/dht-server \
  /ton/build/rldp-http-proxy/rldp-http-proxy \
  /usr/local/bin/

COPY --from=builder /ton/crypto/fift /usr/local/lib/fift
COPY --from=builder /ton/crypto/smartcont /var/ton-work/contracts

WORKDIR /var/ton-work/

ADD /scripts/requirements.txt /var/ton-work/requirements.txt
RUN apt-get update && apt-get install -y gcc libmicrohttpd12 libsecp256k1-dev libsodium-dev && apt-mark manual libmicrohttpd12 &&\
  PIP_NO_CACHE_DIR=1 pip install -r /var/ton-work/requirements.txt && \
  apt-get remove -y gcc && \
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN ln -s /lib/x86_64-linux-gnu/libsecp256k1.so.1.0.0 /usr/lib/libsecp256k1.so.0

ADD ./contracts/gen-zerostate.fif /var/ton-work/contracts
ADD ./contracts/wallet.fif /var/ton-work/contracts/valik-wallet.fif
COPY --from=builder /ton/build/crypto/create-state /var/ton-work/contracts
ADD ./scripts/ /var/ton-work/scripts/


ENTRYPOINT ["python3", "/var/ton-work/scripts/init_ton.py"]
