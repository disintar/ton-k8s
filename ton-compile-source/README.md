# Telegram Open Network Node Container
Dockerfile for running general TON node (works for many testnet). Read more on [TCF Hackermd](https://hackmd.io/@tcf/ByJ0O7CDL).

#### Build container
```bash
git clone https://github.com/TON-Community-Foundation/general-ton-node
cd general-ton-node
docker build -t username/general-ton-node:0.5.0 .
```

This will take some time to compile TON node. Alternatively, you may pull compilled container.
#### Pull container
```docker pull kaemel/general-ton-node:0.5.0```
#### Create volume
```docker volume create ton-db```
#### Run full node
Note, you may need to change IP and used ports. If you don't need Liteserver, then remove `-e "LITESERVER=true"`.

TCF testnet:
```bash
docker run -d --name tcfnet-node --mount source=ton-db,target=/var/ton-work/db --network host -e "PUBLIC_IP=0.0.0.0" -e "CONFIG=https://raw.githubusercontent.com/TON-Community-Foundation/general-ton-node/master/tcf-testnet.config.json"" -e "CONSOLE_PORT=46731" -e "LITESERVER=true" -e "LITE_PORT=46732" -it kaemel/general-ton-node:0.5.0
```

Telegram testnet2:
```bash
docker run -d --name rubynet-node --mount source=ton-db,target=/var/ton-work/db --network host -e "PUBLIC_IP=0.0.0.0" -e "CONFIG=https://test.ton.org/ton-global.config.json" -e "CONSOLE_PORT=46731" -e "LITESERVER=true" -e "LITE_PORT=46732" -it kaemel/general-ton-node:0.5.0
```

Rubynet (by TonLabs):
```bash
docker run -d --name rubynet-node --mount source=ton-db,target=/var/ton-work/db --network host -e "PUBLIC_IP=0.0.0.0" -e "CONFIG=https://raw.githubusercontent.com/tonlabs/net.ton.dev/master/configs/ton-global.config.json" -e "CONSOLE_PORT=46731" -e "LITESERVER=true" -e "LITE_PORT=46732" -it kaemel/general-ton-node:0.5.0
```
#### Run validator
Because TCF Testnet is working on the same code base as TON Testnet, to become validator you can use [Validator HOWTO](https://test.ton.org/Validator-HOWTO.txt).

Also, this image provides ready autovalidation scripts. To use them you need to do the following steps:
1. Enter docker container (`docker exec -it container_name /bin/bash`)
2. Create Validator wallet: (`cd /var/ton-work/contracts && fift -s new-wallet.fif -1 validator`)
3. Get grams for validation stake onto validator wallet
4. Deploy validator wallet (`cd /var/ton-work/contracts && lite-client -C ../db/my-ton-global.config.json -c "sendfile validator-query.boc"`)
5. Adjust parameters of autovalidation scripts, in particular you need to update `WALLET_ADDR`, `MAX_FACTOR` and `STAKE_AMOUNT` in `/var/ton-work/contracts/validator_scripts/participate.sh` and `/var/ton-work/contracts/validator_scripts/reap.sh`
6. Run `participate.sh` and `reap.sh` manually or using cron.

#### validator-engine-console
```bash
docker exec -ti <container-id> /bin/bash```

validator-engine-console -k client -p server.pub -a <IP>:<CONSOLE_PORT>
```
You may use validator-engine-console from other hosts if you copy `client` privkey and `server.pub` pubkey.
#### lite-client
```bash
docker exec -ti <container-id> /bin/bash
lite-client -C my-ton-global.config.json
```

You may use lite-client from other hosts if you copy `my-ton-global.config.json`. Alternatively, if you want to use your own liteserver, copy `liteserver.pub` and run lite-client as follows:

```bash
lite-client -a <IP>:LITE_PORT -p liteserver.pub
```
