ARG is_ssh=false

FROM python:3.10-bullseye AS base

RUN apt-get update && \
        apt-get install -y build-essential cmake clang-11 openssl libssl-dev zlib1g-dev gperf wget git openssl wget python nano && \
        rm -rf /var/lib/apt/lists/*
ENV CMAKE_C_COMPILER clang-11.0
ENV CMAKE_CXX_COMPILER clang++-11.0
WORKDIR /

FROM base AS base-ssh-true
RUN mkdir /root/.ssh
ADD keys/id_rsa /root/.ssh/id_rsa
ADD keys/id_rsa.pub /root/.ssh/id_rsa.pub
ADD keys/known_hosts /root/.ssh/known_hosts

RUN echo "    IdentityFile /root/.ssh/id_rsa" >> /etc/ssh/ssh_config && cat /root/.ssh/id_rsa.pub && \
		chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

FROM base AS base-ssh-false

FROM base-ssh-${is_ssh}
ARG repo
RUN git clone --recursive $repo

WORKDIR /ton
RUN git submodule update

ARG is_testnet
RUN if $is_testnet; then git checkout testnet; fi

RUN mkdir build && \
	cd build && \
	cmake .. -DCMAKE_BUILD_TYPE=Release && \
	make -j $(nproc)

