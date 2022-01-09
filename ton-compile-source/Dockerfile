FROM ubuntu:18.04 as builder
RUN apt-get update && \
	apt-get install -y build-essential cmake clang-6.0 openssl libssl-dev zlib1g-dev gperf wget git openssl wget python nano && \
	rm -rf /var/lib/apt/lists/*
ENV CC clang-6.0
ENV CXX clang++-6.0
WORKDIR /
RUN git clone --recursive https://github.com/newton-blockchain/ton 
WORKDIR /ton

RUN mkdir build && \
	cd build && \
	cmake .. -DCMAKE_BUILD_TYPE=Release && \
	make -j 4

RUN mkdir -p /var/ton-work/db && \
	mkdir -p /var/ton-work/db/static

RUN cp /ton/build/lite-client/lite-client /usr/local/bin/
RUN cp /ton/build/validator-engine/validator-engine /usr/local/bin/
RUN cp /ton/build/validator-engine-console/validator-engine-console /usr/local/bin/
RUN cp /ton/build/utils/generate-random-id /usr/local/bin/

RUN cp /ton/build/test-ton-collator /usr/local/bin
RUN cp /ton/build/crypto/fift /usr/local/bin
RUN cp /ton/build/crypto/func /usr/local/bin
RUN mkdir /usr/local/lib/fift
ENV FIFTPATH /usr/local/lib/fift
RUN cp /ton/crypto/fift/lib /usr/local/lib/fift
RUN mkdir /var/ton-work/contracts
RUN cp /ton/crypto/smartcont /var/ton-work/contracts
RUN cp /ton/build/crypto/create-state /var/ton-work/contracts
RUN cp /ton/build/dht-server/dht-server /usr/local/bin

RUN mkdir -p /var/ton-work/db/keyring
WORKDIR /var/ton-work/contracts
RUN cp gen-zerostate.fif ./
WORKDIR /var/ton-work/db
RUN cp ton-private-testnet.config.json.template node_init.sh control.template prepare_network.sh init.sh clean_all.sh example.config.json ./
ADD validator_scripts /var/ton-work/validator_scripts
RUN chmod +x node_init.sh prepare_network.sh init.sh clean_all.sh

ENTRYPOINT ["/var/ton-work/db/init.sh"]
