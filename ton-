FROM ubuntu:18.04 as builder
RUN apt-get update && \
 apt-get install -y build-essential cmake clang-6.0 openssl libssl-dev zlib1g-dev gperf wget git && \
 rm -rf /var/lib/apt/lists/*
ENV CC clang-6.0
ENV CXX clang++-6.0
WORKDIR /
RUN git clone --recursive https://github.com/newton-blockchain/ton
WORKDIR /ton

RUN mkdir build && \
 cd build && \
 cmake .. -DCMAKE_BUILD_TYPE=Release && \
 cmake --build . --target rldp-http-proxy

FROM ubuntu:18.04
RUN apt-get update && \
 apt-get install -y openssl wget&& \
 rm -rf /var/lib/apt/lists/*

COPY --from=builder /ton/build/rldp-http-proxy/rldp-http-proxy /usr/local/bin/
RUN cd /usr/local/bin/ && wget https://newton-blockchain.github.io/global.config.json

ENTRYPOINT ["rldp-http-proxy"]
