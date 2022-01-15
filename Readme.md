# ton-k8s

Набор докер образов и helm чарт для поднятия комфортной инфраструктуры для работы с [TON](https://ton.org)

`pre-build.sh` - собирает все образы и отправляет их в docker-registry

`ton-compile-source` - основной докер образ который клонит `https://github.com/newton-blockchain/ton/` и компилирует
его. При сборке доступен аргумент `is_testnet`. Если он `true` - клонирует и собирает `safer_overlay` ветку,
т.к. [тестнет работает на ней](https://t.me/testnetstatus/3).

`ton-full-node` - образ full node тона. Очень требователен к ресурсам, так что будьте осторожны :)

## Features

- Full node for mainnet / testnet 💾 [100%]
- Lite-client for mainnet / testnet 🎮 [100%]
- K8s / docker-compose support 🦾 [50%]
- You can change resource limit for nodes in helm values 🚀 [0%]
- Save keys as k8s secret 🔒 [50%]
- Custom private TON network [0%]
- Status page for all networks running [0%]
- TON proxy with k8s ingress and site publish [0%]

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