# ton-k8s

Набор докер образов и helm чарт для поднятия комфортной инфраструктуры для работы с [TON](https://ton.org)

`pre-build.sh` - собирает все образы и отправляет их в docker-registry

`ton-compile-source` - основной докер образ который клонит `https://github.com/newton-blockchain/ton/` и компилирует его. 
При сборке доступен аргумент `is_testnet`. Если он `true` - клонирует и собирает `safer_overlay` ветку, т.к. [тестнет работает на ней](https://t.me/testnetstatus/3).

`ton-full-node` - образ full node тона. Очень требователен к ресурсам, так что будьте осторожны :)


## Helm / k8s

You need to change `./chart/values.yaml`

Then:

```bash
kubectl create namespace ton
helm upgrade --install --namespace ton ton ./chart/ --values ./chart/values.yaml 
```