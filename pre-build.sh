export REGISTRY=registry.head-labs.com
export VERSION=v0

# Build base compile source

cd ton-compile-source

docker build -f Dockerfile -t ton-base . --build-arg is_testnet=false
docker tag ton-base ${REGISTRY}/ton/ton-base:mainnet-${VERSION}
docker push ${REGISTRY}/ton/ton-base:mainnet-${VERSION}

docker build -f Dockerfile -t ton-base . --build-arg is_testnet=true
docker tag ton-base ${REGISTRY}/ton/ton-base:testnet-${VERSION}
docker push ${REGISTRY}/ton/ton-base:testnet-${VERSION}

cd ../ton-full-node

docker build -f Dockerfile -t ton-node . --build-arg version=mainnet-${VERSION}
docker tag ton-base ${REGISTRY}/ton/ton-node:mainnet-${VERSION}
docker push ${REGISTRY}/ton/ton-node:mainnet-${VERSION}

docker build -f Dockerfile -t ton-node . --build-arg version=testnet-${VERSION}
docker tag ton-base ${REGISTRY}/ton/ton-node:testnet-${VERSION}
docker push ${REGISTRY}/ton/ton-node:testnet-${VERSION}
