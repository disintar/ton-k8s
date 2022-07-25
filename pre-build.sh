#!/bin/bash

cd ton-compile-source || return

docker build -f Dockerfile -t ton-base-mainnet . --build-arg is_testnet=false --build-arg repo=https://github.com/ton-blockchain/ton.git
docker build -f Dockerfile -t ton-base-testnet . --build-arg is_testnet=true --build-arg repo=https://github.com/ton-blockchain/ton.git

cd ../ton-full-node || return

docker build -f Dockerfile -t ton-node-mainnet . --build-arg base=ton-base-mainnet
docker build -f Dockerfile -t ton-node-testnet . --build-arg base=ton-base-testnet

cd ../ton-http-config || return

docker build -f Dockerfile -t ton-http-config . --build-arg base=ton-base-mainnet

cd ../ton-toncenter || return

docker build -f Dockerfile -t ton-toncenter-mainnet . --build-arg base=ton-base-mainnet
docker build -f Dockerfile -t ton-toncenter-testnet . --build-arg base=ton-base-testnet

cd ..
