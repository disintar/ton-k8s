export REGISTRY=registry.head-labs.com
export VERSION=v0

# Build base compile source

cd ton-compile-source

docker build -f Dockerfile -t ton-base .
docker tag ton-base ${REGISTRY}/ton/ton-base:${VERSION}
docker push ${REGISTRY}/ton/ton-base:${VERSION}

cd ../ton-full-node
docker build -f Dockerfile -t ton-node .
docker tag ton-base ${REGISTRY}/ton/ton-node:${VERSION}
docker push ${REGISTRY}/ton/ton-node:${VERSION}