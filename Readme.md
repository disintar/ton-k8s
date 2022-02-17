# ton-k8s

Docker images, python mini-lib, helm chart for comfortable [TON](https://ton.org) infrastructure

## Features

| Feature name                      | Status |
|-----------------------------------|--------|
| Full node for mainnet / testnet   | ✅      |
| Lite-client for mainnet / testnet | ✅      |
| Helm chart                        | ✅      |
| K8s secrets for keys              | ✅      |
| Custom ton network                | ⌛      |
| Status page                       | ⌛      |
| K8s resource limits               | ⌛      |
| RPC API                           | ⌛      |


### Files

`pre-build.sh` - build all docker files and send them to registry

`ton-compile-source` - main Docker image, compile [TON](`https://github.com/newton-blockchain/ton/`) sources. You can
pass`is_testnet`. If `true` - compile and build `safer_overlay` branch,
because [testnet is working on it](https://t.me/testnetstatus/3).

`ton-full-node` - run mainnet / testnet full node, you need to pass `version` build argument `mainnet-v0`
or `testnet-v0`

## Helm / k8s

You need to change `./chart/values.yaml`

Then:

```bash
kubectl create namespace ton
helm upgrade --install --namespace ton ton ./chart/ --values ./chart/values.yaml 
```

### Tips and tricks

After publish UDP services to k8s you need to specify `externalIp` to bind public port.
[Read more about externalIp](https://kubernetes.io/docs/concepts/services-networking/service/#external-ips)