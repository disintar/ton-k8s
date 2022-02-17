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
| Compose                           | ⌛      |
| RPC API                           | ⌛      |

### Local build

It's one of the easiest way to start TON network locally:

```
./pre-build.sh
```

### Files

`pre-build.sh` - build all docker files and send them to registry

`ton-compile-source` - main Docker image, compile [TON](`https://github.com/newton-blockchain/ton/`) sources. You can
pass`is_testnet`. If `true` - compile and build `safer_overlay` branch,
because [testnet is working on it](https://t.me/testnetstatus/3).

`ton-full-node` - run mainnet / testnet full node, you need to pass `version` build argument `mainnet-v0`
or `testnet-v0`

## Helm / k8s

1. Change registry in build_for_k8s.sh
2. Run build_for_k8s.sh and push images to registry
3. Change `./chart/values.yaml` to specify your needs

Then:

```bash
kubectl create namespace ton
helm upgrade --install --namespace ton ton ./chart/ --values ./chart/values.yaml 
```

### Tips and tricks

After publish UDP services to k8s you need to specify `externalIp` to bind public port.
[Read more about externalIp](https://kubernetes.io/docs/concepts/services-networking/service/#external-ips)

## ENVIRON

Feel free to change environs in compose / helm

```
config = {
    "PUBLIC_IP": ip,
    "CONFIG": os.getenv('CONFIG', 'https://test.ton.org/ton-global.config.json'),
    "PRIVATE_CONFIG": os.getenv('PRIVATE_CONFIG', 'false') == 'true',
    "LITESERVER": os.getenv('LITESERVER', 'true') == 'true',  # convert to bool
    "CONSOLE_PORT": int(os.getenv("CONSOLE_PORT", 46732)),
    "PUBLIC_PORT": int(os.getenv("PUBLIC_PORT", 50001)),
    "DHT_PORT": int(os.getenv("DHT_PORT", 6302)),
    "LITESERVER_PORT": int(os.getenv("LITESERVER_PORT", 43680)),
    "NAMESPACE": os.getenv("NAMESPACE", None),
    "THREADS": int(os.getenv("CPU_COUNT", cpu_count)),
    "GENESIS": os.getenv("GENESIS", False),
    "VERBOSE": os.getenv("VERBOSE", 3)
}
```