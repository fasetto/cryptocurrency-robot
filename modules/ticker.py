
from enum import Enum, unique
import json
import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://min-api.cryptocompare.com/data/generateAvg?fsym=%s&tsym=%s&markets=%s"
KOIMIM_URL = "https://koinim.com/ticker/"

@unique
class Markets(Enum):
    Paribu = 'Paribu'
    Koinim = 'Koinim'
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
        self._market = None
        self._couple = None

    @property
    def pair(self):
        return self._couple
    
    @pair.setter
    def pair(self, value):
        self._couple = value
        return self._couple

    @property
    def market(self):
        return self._market
    
    @market.setter
    def market(self, value):
        self._market = value
        return self._market

    def ticker(self):
        couple = self._couple.split('/')
        request_url = BASE_URL % (couple[0], couple[1], self._market.value)
        result = self.__api_call(request_url)

        try:
            if self.market == Markets.Koinim and self.pair == 'BTC/TRY':
                result = {
                    'price': "₺ {:,.2f}".format(result['last_order']),
                    'volume24h': "Ƀ {:,.2f}".format(result['volume']),
                    'open24h': 'NaN',
                    'high24h': "₺ {:,.2f}".format(result['high']),
                    'low24h': "₺ {:,.2f}".format(result['low']),
                    'change24h': "% {:.2f}".format(result['change_rate'])
                }
                return result
            elif self.market == Markets.Paribu and self.pair == 'BTC/TRY':
                return self.paribu_ticker()

            result = {
                'price': result['DISPLAY']['PRICE'],
                'volume24h': result['DISPLAY']['VOLUME24HOUR'],
                'open24h': result['DISPLAY']['OPEN24HOUR'],
                'high24h': result['DISPLAY']['HIGH24HOUR'],
                'low24h': result['DISPLAY']['LOW24HOUR'],
                'change24h': result['DISPLAY']['CHANGE24HOUR']
            }



        except KeyError:
            return None

        return result

    def paribu_ticker(self):
        html_doc = requests.get('https://www.paribu.com').text
        soup = BeautifulSoup(html_doc, 'html.parser')
        js_text = soup.find('script', type="text/javascript").text
        regex =  re.compile('("day_stats"):(.*?)$|,', re.MULTILINE)
        js_text = re.findall(regex, js_text)[7][1]
        result = json.loads(re.sub("}}};", "", js_text))

        result = {
            'price': "₺ {:,.2f}".format(result['lst']),
            'volume24h': "NaN",
            'open24h': 'NaN',
            'high24h': "₺ {:,.2f}".format(result['max']),
            'low24h': "₺ {:,.2f}".format(result['min']),
            'change24h': "₺ {:.2f}".format(result['chg'])
        }
        return result

    def __api_call(self, uri):
        if self.market == Markets.Koinim:
            result = requests.get(KOIMIM_URL).json()
            return result

        result = requests.get(uri).json()
        return result
