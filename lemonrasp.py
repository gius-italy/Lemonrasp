#!/usr/bin/env python3
# coding: utf8

import json
import logging
import os
import requests
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


admin_chatId=42424242
bot_token="444333222:hellomysupersecretbotTokenisthisone!"



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Ciaone!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Comandi disponibili:\n'
        '/ngrok_start Esegue ngrok e stampa\n\tl\'url e la porta assegnata\n'
        '/ngrok_stop Termina l\'esecuzione di ngrok')


def echo(bot, update):
    """Echo the user message."""
        update.message.reply_text("Ci sono!")

def ngrok_start(bot,update):
    ngrok_api_url="http://127.0.1:4040/api/tunnels"
    if update.message.chat_id==admin_chatId:
        os.system("/home/pi/ngrok tcp 20806 &")
        time.sleep(2) #Give ngrok time to open the tunnel
        resp=requests.get(ngrok_api_url)
        public_url=json.loads(resp.text)['tunnels'][0]['public_url']
        port=public_url.split(':')[2]
        public_url=public_url.split('//')[1].split(':')[0]
        update.message.reply_text('Ngrok')
        update.message.reply_text('Public url : '+public_url)
        update.message.reply_text('Port : '+port)
    else:
        update.message.reply_text('Mi dispiace, non hai i permessi per eseguire '
                'questo comando!')



def ngrok_stop(bot,update):
    if update.message.chat_id==admin_chatId:
        os.system("killall -s SIGINT ngrok")
        update.message.reply_text('Ngrok tunnel closed!')
    else:
        update.message.reply_text('Mi dispiace, non hai i permessi per eseguire '
                'questo comando!')

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ngrok_start", ngrok_start))
    dp.add_handler(CommandHandler("ngrok_stop", ngrok_stop))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
