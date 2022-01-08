export REGISTRY = registry.head-labs.com
export VERSION = v0

cd ton-compile-source

docker build -f Dockerfile -t ton-base .
docker tag ton-base:latest ${REGISTRY}/ton/ton-base:${VERSION}
docker push registry.head-labs.com/ton/ton-base:${VERSION}



