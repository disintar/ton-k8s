FROM python:3.7-bullseye

RUN apt-get update && \
        apt-get install -y build-essential cmake clang-11 openssl libssl-dev zlib1g-dev gperf wget git openssl wget python nano && \
        rm -rf /var/lib/apt/lists/*
ENV CMAKE_C_COMPILER clang-11.0
ENV CMAKE_CXX_COMPILER clang++-11.0
WORKDIR /

RUN mkdir /root/.ssh
ADD keys/id_rsa /root/.ssh/id_rsa
ADD keys/id_rsa.pub /root/.ssh/id_rsa.pub

RUN  echo "    IdentityFile /root/.ssh/id_rsa" >> /etc/ssh/ssh_config && cat /root/.ssh/id_rsa.pub
RUN ssh-keyscan -t rsa -p 228 git.head-labs.com >> ~/.ssh/known_hosts && chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

RUN git clone --recursive ssh://git@git.head-labs.com:228/disintar/ton.git

WORKDIR /ton
RUN git submodule update

ARG is_testnet
RUN if $is_testnet; then git checkout testnet; fi

RUN mkdir build && \
	cd build && \
	cmake .. -DCMAKE_BUILD_TYPE=Release && \
	make -j 24

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
RUN cp -r /ton/crypto/fift/lib /usr/local/lib/fift
RUN mkdir /var/ton-work/contracts
RUN cp -r /ton/crypto/smartcont/* /var/ton-work/contracts
RUN cp /ton/build/dht-server/dht-server /usr/local/bin
RUN cp /ton/build/rldp-http-proxy/rldp-http-proxy /usr/local/bin

WORKDIR /var/ton-work/

RUN mkdir /var/ton-work/scripts
COPY ./scripts/requirements.txt /var/ton-work/
RUN pip install -r /var/ton-work/requirements.txt

ADD ./contracts/gen-zerostate.fif /var/ton-work/contracts
ADD ./contracts/wallet.fif /var/ton-work/contracts/valik-wallet.fif
RUN cp /ton/build/crypto/create-state /var/ton-work/contracts
ADD ./scripts/ /var/ton-work/scripts/
