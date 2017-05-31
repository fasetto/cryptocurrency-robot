
import os
from enum import Enum, unique
import json
import requests

BASE_URL = "https://min-api.cryptocompare.com/data/generateAvg?fsym=%s&tsym=%s&markets=%s"
# https://min-api.cryptocompare.com/data/generateAvg?fsym=BTC&tsym=USD&markets=Cexio"

@unique
class Markets(Enum):
    Cexio = 'Cexio'
    Bitstamp = 'Bitstamp'
    Bitfinex = 'Bitfinex'
    Poloniex = 'Poloniex'
    BTCE = 'BTCE'
    OKCoin = 'OKCoin'
    Coinbase = 'Coinbase'
    Kraken = 'Kraken'

class Ticker:
    '''Ticker api for some popular markets.'''
    def __init__(self):
        pass

    def ticker(self, market, couple):
        couple = couple.split('/')
        request_url = BASE_URL % (couple[0], couple[1], market.value)
        result = self.__api_call(request_url)

        result = {
            'price': result['RAW']['PRICE'],
            'volume24h': result['RAW']['VOLUME24HOUR'],
            'open24h': result['RAW']['OPEN24HOUR'],
            'high24h': result['RAW']['HIGH24HOUR'],
            'low24h': result['RAW']['LOW24HOUR'],
            'change24h': result['RAW']['CHANGE24HOUR']
        }
        return result

    def __api_call(self, uri):
        result = requests.get(uri).json()
        return result
