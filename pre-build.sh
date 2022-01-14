export REGISTRY=registry.head-labs.com
export PUSH_TO_REGISTRY=false
export VERSION=v0

# Build base compile source

cd ton-compile-source

docker build -f Dockerfile -t ton-base-mainnet . --build-arg is_testnet=false

if PUSH_TO_REGISTRY; then
  docker tag ton-base-mainnet ${REGISTRY}/ton/ton-base:mainnet-${VERSION}
  docker push ${REGISTRY}/ton/ton-base:mainnet-${VERSION}
fi;

docker build -f Dockerfile -t ton-base-testnet . --build-arg is_testnet=true

if PUSH_TO_REGISTRY; then
  docker tag ton-base-testnet ${REGISTRY}/ton/ton-base:testnet-${VERSION}
  docker push ${REGISTRY}/ton/ton-base:testnet-${VERSION}
fi;

cd ../ton-full-node

docker build -f Dockerfile -t ton-node-mainnet . --build-arg version=mainnet-${VERSION}

if PUSH_TO_REGISTRY; then
  docker tag ton-node-mainnet ${REGISTRY}/ton/ton-node:mainnet-${VERSION}
  docker push ${REGISTRY}/ton/ton-node:mainnet-${VERSION}
fi;

docker build -f Dockerfile -t ton-node-testnet . --build-arg version=testnet-${VERSION}

if PUSH_TO_REGISTRY; then
  docker tag ton-node-testnet ${REGISTRY}/ton/ton-node:testnet-${VERSION}
  docker push ${REGISTRY}/ton/ton-node:testnet-${VERSION}
fi;