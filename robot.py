
import logging
import gettext

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters,
    RegexHandler, ConversationHandler
)

from modules import config

t = gettext.translation('robot', localedir='./locales', languages=['tr_TR'])

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger('CryptoCurrency Bot')

LANGUAGE = range(1)

def start(bot, update):
    user = update.message.from_user
    reply_keyboard = [['🇬🇧 English', '🇹🇷 Türkçe']]

    update.message.reply_text(
        _("%s, choose your language.", user.id) % user.first_name,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    )

    return LANGUAGE

def _(message, user_id):
    translate = t.gettext
    lang = config.language(user_id)

    if lang == 'ENG':
        return message

    return translate(message)

def language(bot, update):
    user = update.message.from_user
    lang = 'ENG' if 'English' in update.message.text else 'TR'

    config.write(user.id, language=lang, user=user.first_name)

    logger.info("Language of %s: %s", user.first_name, update.message.text)


    update.message.reply_text(
        _("Perfect, your language is set: %s", user.id) % update.message.text,
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    return ConversationHandler.END

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

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
