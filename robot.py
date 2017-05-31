
import logging
import gettext

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (
    Updater, CommandHandler,
    RegexHandler, ConversationHandler
)

from modules import config
from modules.ticker import Ticker, Markets

t = gettext.translation('robot', localedir='./locales', languages=['tr_TR'])

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m-%d-%Y %I:%M:%S %p',
                    level=logging.INFO)

logger = logging.getLogger('CryptoCurrency Bot')
logger.addHandler(logging.FileHandler('.log', encoding='utf-8'))

LANGUAGE = 0
PAIR, MARKET = range(2)

tickr = Ticker()

def start(bot, update):
    user = update.message.from_user
    reply_keyboard = [['🇬🇧 English', '🇹🇷 Türkçe']]

    update.message.reply_text(
        _("%s, choose your language.", user.id) % user.first_name,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, 
                                         resize_keyboard=True, 
                                         one_time_keyboard=True)
    )

    return LANGUAGE

def language(bot, update):
    user = update.message.from_user
    lang = 'ENG' if 'English' in update.message.text else 'TR'

    config.write(user.id, language=lang, user=user.first_name)

    logger.info("Language of %s: %s", user.first_name, update.message.text)


    update.message.reply_text(
        _("Perfect, your language is set: %s", user.id) % update.message.text,
        reply_markup=ReplyKeyboardRemove()
    )

    return -1

def ticker(bot, update):
    user = update.message.from_user
    reply_keyboard = [['BTC/USD', 'BTC/EUR'],
                      ['ETH/USD', 'ETH/BTC'],
                      ['ETC/USD', 'ETC/BTC'],
                      ['LTC/USD', 'LTC/BTC'],
                      ['XRP/USD', 'XRP/BTC'],
                      ['XMR/USD', 'XMR/BTC']]

    update.message.reply_text(
        _("Choose a pair.", user.id),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, 
                                         resize_keyboard=True, 
                                         one_time_keyboard=True)
    )

    return PAIR

def pair(bot, update):
    user = update.message.from_user
    couple = update.message.text
    reply_keyboard = [['⬅️ Back'],
                      ['Paribu', 'Koinim'],
                      ['Bitstamp', 'Bitfinex'],
                      ['Cexio', 'Poloniex'],
                      ['Coinbase', 'Kraken'],
                      ['BTCE', 'OKCoin']]

    tickr.pair = couple

    update.message.reply_text(
        _("Now choose a market.", user.id),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                         resize_keyboard=True,
                                         one_time_keyboard=True)
    )

    return MARKET

def market(bot, update):
    user = update.message.from_user
    market = update.message.text

    if market == '⬅️ Back':
        return ticker(bot, update)

    tickr.market = Markets[market]
    market_ticker = tickr.ticker()

    if market_ticker is None:
        update.message.reply_text(_("Unsupported pair.", user.id))

    update.message.reply_text(
        _("Price: {} \n"
          "Open: {}\n"
          "24h High: {}\n"
          "24h Low: {}\n"
          "24h Volume: {}\n"
          "24h Change: {}", user.id).format(market_ticker['price'], 
                                            market_ticker['open24h'],
                                            market_ticker['high24h'],
                                            market_ticker['low24h'],
                                            market_ticker['volume24h'],
                                            market_ticker['change24h']),
    )


def _(message, user_id):
    translate = t.gettext
    lang = config.language(user_id)

    if lang == 'ENG':
        return message

    return translate(message)

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    update.message.reply_text(
        _("", user.id),
        reply_markup=ReplyKeyboardRemove()
    )
    return -1

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    updater = Updater(config.token)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        
        states={
            LANGUAGE: [RegexHandler('^(🇬🇧 English|🇹🇷 Türkçe)', language)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    ticker_handler = ConversationHandler(
        entry_points=[CommandHandler('ticker', ticker)],

        states={
            PAIR: [RegexHandler('^(BTC/USD|BTC/EUR|ETH/USD|ETH/BTC|ETC/USD|ETC/BTC|LTC/USD|LTC/BTC|XRP/USD|XRP/BTC|XMR/USD|XMR/BTC)', pair)],
            MARKET: [RegexHandler('^(⬅️ Back|Paribu|Koinim|Bitstamp|Bitfinex|Cexio|Poloniex|Coinbase|Kraken|BTCE|OKCoin)', market)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(ticker_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
