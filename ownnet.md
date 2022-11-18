### Info about running ownnet

After you start your ownnet, you need to access wallet to get funds. First thing you need to do is get your private key
```
curl -s http://localhost:8081/valik.pk?token=secret
```
(token is SHARED_SECRET env variable)

In response you'll get base64 seed of the key. To access wallets you need to know their walletId and address.

```
address,walletId
-1:1111111111111111111111111111111111111111111111111111111111111110,1
-1:111111111111111111111111111111111111111111111111111111111111110F,2
```

Example of sending funds in js:
```javascript
import BN from 'bn.js'
import { keyPairFromSeed } from 'ton-crypto'
import TonWeb from 'tonweb'

async function main() {
  // secret key is the key you got from valik.pk
  const secretKey = Buffer.from('D7eJFoDNIbyWVhmcd4G8D0I5jFzMu3ZiK6GmDGNKdNc=', 'base64')
  const keyPair = keyPairFromSeed(secretKey)

  const wallet = new TonWeb.Wallets.all.v3R2(
      new TonWeb.HttpProvider('http://localhost:8082/jsonRPC'),
      {
        address: '-1:1111111111111111111111111111111111111111111111111111111111111110',
        publicKey: keyPair.publicKey,
        walletId: 1,
        wc: -1,
      }
    )
  const seqno = (await wallet.methods.seqno().call()) || 0
  const res = await wallet.methods
    .transfer({
      seqno,
      secretKey: keyPair.secretKey,
      toAddress: '-1:111111111111111111111111111111111111111111111111111111111111110F',
      amount: new BN(100000000000),
    })
    .send()
  console.log('res', res)
}
main()
```
