
import logging
import gettext

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (
    Updater, CommandHandler, Job,
    RegexHandler, ConversationHandler
)
from telegram.ext.dispatcher import run_async

from modules import config
from modules.ticker import Ticker, Markets

t = gettext.translation('robot', localedir='./locales', languages=['tr_TR'])

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m-%d-%Y %I:%M:%S %p',
                    level=logging.INFO)

logger = logging.getLogger('CryptoCurrency Bot')
logger.addHandler(logging.FileHandler('.log', encoding='utf-8'))

JOBS = []
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
        _("@ {}\n"
          "Price: {}\n"
          "Open: {}\n"
          "24h High: {}\n"
          "24h Low: {}\n"
          "24h Volume: {}\n"
          "24h Change: {}", user.id).format(tickr.market.value,
                                            market_ticker['price'], 
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

@run_async
def notify_callback(bot, job):
    market = job.context['market']
    pair = job.context['pair']
    condition = job.context['condition'].split('=')[0]
    condition_price = float(job.context['condition'].split('=')[1])

    tickr.market = Markets[market]
    tickr.pair = pair
    last_price = float(tickr.ticker()['price'].split(' ')[1].replace(',', '.'))

    if condition == '>':
        if last_price > condition_price:
            bot.send_message(job.context['chat_id'], text='Alarm: Last price: %s' % last_price)
    elif condition == '<':
        if last_price < condition_price:
            bot.send_message(job.context['chat_id'], text='Alarm: Last price: %s' % last_price)

def notify(bot, update, args, job_queue, chat_data):
    chat_id = update.message.chat_id

    if args[0] == 'pop':
        try:
            _job = JOBS[-1]
        except IndexError:
            update.message.reply_text('You have no active alarm.')
            return

        _job.schedule_removal()
        JOBS.pop()
        update.message.reply_text('Alarm successfully removed !')
        return

    try:
        arguments = {
            'chat_id': chat_id, 
            'market': args[0], 
            'pair': args[1],
            'condition': args[2]
        }

        job = job_queue.run_repeating(notify_callback, 10.0, context=arguments)
        JOBS.append(job)

        update.message.reply_text('I will notify you ! (:')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /notify market pair >=value')

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
    dp.add_handler(CommandHandler("notify", notify,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
