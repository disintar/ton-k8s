#!/bin/bash

export REGISTRY=registry.head-labs.com
export VERSION=v1

# Build base compile source

cd ton-compile-source || return

# mainnet
docker build -f Dockerfile -t ton-base-mainnet . --build-arg is_testnet=false

docker tag ton-base-mainnet ${REGISTRY}/ton/ton-base:mainnet-${VERSION}
docker push ${REGISTRY}/ton/ton-base:mainnet-${VERSION}

# testnet
docker build -f Dockerfile -t ton-base-testnet . --build-arg is_testnet=true

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
