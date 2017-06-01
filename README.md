
# CryptoCurrency Bot

Provides informations about *cryptocurrencies*.
To get this bot click [here][bot-url].

## Commands

- `/start ` to initialize the bot
- `/ticker` to get ticker
- `/notify` to receive notifications from market
- `/cancel` cancel current operation
- `/help` to see all available commands

## Notify command

Usage: `/notify <market> <pair> <condition> <price>`

### params
- **market** -> Like *Paribu*, *Koinim*, *Poloniex*, *Cexio*, ..etc can be all supported markets.
- **pair** -> Like *BTC/TRY*, *BTC/USD*, *ETH/USD*, ..etc
- **condition** -> `<` or `>`
- **price** -> decimal value
### example
`/notify Paribu BTC/TRY < 8500`

## Screenshots

![screenshot1](screenshots/bot.png)

![screenshot2](screenshots/bot2.png)

[bot-url]: <https://telegram.me/cryptocurrencyrobot>
