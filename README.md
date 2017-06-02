
# CryptoCurrency Bot

Provides informations about *cryptocurrencies*.
To get to this bot click [telegram.me/cryptocurrencyrobot][bot-url].

## Commands

- `/start ` to initialize the bot
- `/ticker` to get ticker
- `/notify` to receive notifications from market
- `/cancel` cancel current operation
- `/help` to see all available commands

## Notify command

Usage for set alarm: `/notify <market> <pair> <condition> <price>` </br>
Usage for remove alarm: `/notify remove`

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
