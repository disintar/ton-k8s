@echo off

docker build -f ton-compile-source/Dockerfile -t ton-base-mainnet ton-compile-source/. --build-arg is_testnet=false --build-arg repo=https://github.com/ton-blockchain/ton.git
docker build -f ton-compile-source/Dockerfile -t ton-base-testnet ton-compile-source/. --build-arg is_testnet=true --build-arg repo=https://github.com/ton-blockchain/ton.git

docker build -f ton-full-node/Dockerfile -t ton-node-mainnet ton-full-node/. --build-arg base=ton-base-mainnet
docker build -f ton-full-node/Dockerfile -t ton-node-testnet ton-full-node/. --build-arg base=ton-base-testnet

docker build -f ton-http-config/Dockerfile -t ton-http-config ton-http-config/. --build-arg base=ton-base-mainnet

docker build -f ton-toncenter/Dockerfile -t ton-toncenter-mainnet ton-toncenter/. --build-arg base=ton-base-mainnet
docker build -f ton-toncenter/Dockerfile -t ton-toncenter-testnet ton-toncenter/. --build-arg base=ton-base-testnet
