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
docker build -f Dockerfile -t ton-node .
docker tag ton-base ${REGISTRY}/ton/ton-node:${VERSION}
docker push ${REGISTRY}/ton/ton-node:${VERSION}