import json
import os
import logging
import requests

from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Config logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# set up telegram bot
telegram_api = os.environ.get('TELEGRAM_API')
updater = Updater(token=telegram_api, use_context=True)
dispatcher = updater.dispatcher

# set up wise
wise_api = os.environ.get('WISE_API')
url = "https://api.transferwise.com/v1/rates?source=EUR&target=HUF"
headers = {'Authorization': f'Bearer {wise_api}'}


def get_reply_keyboard_markup():
    wise_keyboard = [
        [KeyboardButton('Get EUR/HUF'),KeyboardButton('Get EUR/UAH')]
    ]
    return ReplyKeyboardMarkup(wise_keyboard, resize_keyboard=True)


def echo(update, context):
    if update.message.text == 'Get EUR/HUF':
        try:
            data = json.loads(requests.get(url=url, headers=headers).text)[0]
            response = str(data['rate']) + " HUF/EUR"
        except:
            response = "Error loading exchange data."
    else:
        response = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             key=get_reply_keyboard_markup(),
                             text=response)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_markup=get_reply_keyboard_markup(),
                             text="I'm a bot, please talk to me!")
    logging.info(update.effective_chat.id)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# -----------------------------------------------------------------------------
# Run the Bot
logging.info('Bot started')
updater.start_polling()
updater.idle()
