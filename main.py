#!/usr/bin/python3

import configparser
import logging
import importlib
import os
from inspect import getmembers, isfunction
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('./config.ini')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(config['BOT']['TOKEN'], use_context=True)

    dp = updater.dispatcher

    plugins = [p.split('.py')[0] for p in os.listdir(
        './modules') if p != '__init__.py' and p.endswith('.py')]

    for mod in plugins:
        p = importlib.import_module('modules.' + mod)
        for f in p.__all__:
            func = getattr(p, f)
            dp.add_handler(CommandHandler(f, func))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
