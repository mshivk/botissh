#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages. This is built on the telegram.ext part of python-telegram-bot package.
from telegram.ext import Updater,CommandHandler
import mongoConnect 

updater = Updater(token='262220782:AAHUsCJ2kIrw1OBJKjXMSKvq09KpRUatx3M')
dispatcher = updater.dispatcher

def dbupdate(bot,update, text =''):
    dbDoc = {
            'chatId':update.message.chat_id,
            'botRxcved' : update.message.text,
            'botTxed': text,
            'userFn': update.message.chat.first_name,
            'utcnow':update.message.date
             }
    mongoConnect.insertOne(dbDoc)


def starty(bot, update):
    botreply = "I'm a simple bot. Type /joke or whatever!" 
    bot.sendMessage(chat_id=update.message.chat_id, text=botreply)
    dbupdate(bot,update, botreply)

def joke(bot, update):
    botreply = "Today a man knocked on my door and asked for a small donation towards the local swimming pool. I gave him a glass of water."
    bot.sendMessage(chat_id=update.message.chat_id, text=botreply)
    dbupdate(bot,update, botreply)

def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)
    botreply = update.message.text
    dbupdate(bot,update,botreply)

start_handler = CommandHandler('start', starty)
dispatcher.add_handler(start_handler)
joke_handler = CommandHandler('joke', joke)
dispatcher.add_handler(joke_handler)
updater.start_polling()

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler([Filters.text], echo)
dispatcher.add_handler(echo_handler)

updater.idle()

