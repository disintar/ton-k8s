FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
	apt-get install -y build-essential cmake clang openssl libssl-dev \
    libgflags-dev zlib1g-dev libssl-dev libreadline-dev libmicrohttpd-dev pkg-config libgsl-dev \
     zlib1g-dev gperf wget git openssl wget python python3 python3-pip nano vim && \
	rm -rf /var/lib/apt/lists/*

WORKDIR /
RUN git clone --recursive https://github.com/newton-blockchain/ton 
WORKDIR /ton

RUN CC=$(which clang) && CXX=$(which clang++) && CCACHE_DISABLE=1 && \
    mkdir build && \
	cd build && \
	cmake .. -DCMAKE_BUILD_TYPE=Release && \
	make -j 4


RUN mkdir -p /var/ton-work/db && \
	mkdir -p /var/ton-work/db/static

COPY /ton/build/lite-client/lite-client /usr/local/bin/
COPY /ton/build/validator-engine/validator-engine /usr/local/bin/
COPY /ton/build/validator-engine-console/validator-engine-console /usr/local/bin/
COPY /ton/build/utils/generate-random-id /usr/local/bin/

COPY /ton/build/test-ton-collator /usr/local/bin
COPY /ton/build/crypto/fift /usr/local/bin
COPY /ton/build/crypto/func /usr/local/bin
RUN mkdir /usr/local/lib/fift
ENV FIFTPATH /usr/local/lib/fift
COPY /ton/crypto/fift/lib /usr/local/lib/fift
RUN mkdir /var/ton-work/contracts
COPY /ton/crypto/smartcont /var/ton-work/contracts
COPY /ton/build/crypto/create-state /var/ton-work/contracts
COPY /ton/build/dht-server/dht-server /usr/local/bin
COPY /ton/build/rldp-http-proxy/rldp-http-proxy /usr/local/bin

RUN mkdir -p /var/ton-work/db/keyring
WORKDIR /var/ton-work/contracts
COPY gen-zerostate.fif ./
WORKDIR /var/ton-work/db
COPY ton-private-testnet.config.json.template node_init.sh control.template prepare_network.sh init.sh clean_all.sh example.config.json ./
ADD validator_scripts /var/ton-work/validator_scripts
RUN chmod +x node_init.sh prepare_network.sh init.sh clean_all.sh
