#!/bin/bash

export REGISTRY=registry.head-labs.com
export VERSION=v1

# Build base compile source

cd ton-compile-source || return

# mainnet
docker build -f Dockerfile -t ton-base-mainnet . --build-arg is_testnet=false --build-arg repo=ssh://git@git.head-labs.com:228/disintar/ton.git

docker tag ton-base-mainnet ${REGISTRY}/ton/ton-base:mainnet-${VERSION}
docker push ${REGISTRY}/ton/ton-base:mainnet-${VERSION}

# testnet
docker build -f Dockerfile -t ton-base-testnet . --build-arg is_testnet=true --build-arg repo=ssh://git@git.head-labs.com:228/disintar/ton.git

docker tag ton-base-testnet ${REGISTRY}/ton/ton-base:testnet-${VERSION}
docker push ${REGISTRY}/ton/ton-base:testnet-${VERSION}

cd ../ton-full-node || return

# fullnode mainnet
docker build -f Dockerfile -t ton-node-mainnet . --build-arg base=${REGISTRY}/ton/ton-base:mainnet-${VERSION}
docker tag ton-node-mainnet ${REGISTRY}/ton/ton-node:mainnet-${VERSION}
docker push ${REGISTRY}/ton/ton-node:mainnet-${VERSION}

# fullnode testnet
docker build -f Dockerfile -t ton-node-testnet . --build-arg base=${REGISTRY}/ton/ton-base:testnet-${VERSION}
docker tag ton-node-testnet ${REGISTRY}/ton/ton-node:testnet-${VERSION}
docker push ${REGISTRY}/ton/ton-node:testnet-${VERSION}

cd ../ton-http-config || return

# http-config mainnet
docker build -f Dockerfile -t ton-http-config . --build-arg base=${REGISTRY}/ton/ton-base:mainnet-${VERSION}
docker tag ton-http-config ${REGISTRY}/ton/ton-http-config:${VERSION}
docker push ${REGISTRY}/ton/ton-http-config:${VERSION}


cd ../ton-toncenter || return

# toncenter mainnet
docker build -f Dockerfile -t ton-toncenter-mainnet . --build-arg base=${REGISTRY}/ton/ton-base:mainnet-${VERSION}
docker tag ton-toncenter-mainnet ${REGISTRY}/ton/ton-toncenter:mainnet-${VERSION}
docker push ${REGISTRY}/ton/ton-toncenter:mainnet-${VERSION}

# toncenter testnet
docker build -f Dockerfile -t ton-toncenter-testnet . --build-arg base=${REGISTRY}/ton/ton-base:testnet-${VERSION}
docker tag ton-toncenter-testnet ${REGISTRY}/ton/ton-toncenter:testnet-${VERSION}
docker push ${REGISTRY}/ton/ton-toncenter:testnet-${VERSION}
