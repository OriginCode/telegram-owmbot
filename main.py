#!/usr/bin/python3

import json
import logging
import importlib
import os
from inspect import getmembers, isfunction
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

with open('./config.json') as f:
    config = json.load(f)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(config['BOT']['TOKEN'], use_context=True)

    dp = updater.dispatcher

    loaded = []

    # TODO: Better way to load plugins, with different types of handler supported.
    for mod in [p.split('.py')[0] for p in os.listdir('./modules') if p != '__init__.py' and p.endswith('.py')]:
        p = importlib.import_module('modules.' + mod)
        for f in p.__all__:
            loaded.append(f)
            func = getattr(p, f)
            dp.add_handler(CommandHandler(f, func))

    dp.add_handler(
        CommandHandler(
            'plugins',
            lambda update, context:
            update.message.reply_text(
                '*Loaded Plugins*\n' + ', '.join(loaded),
                parse_mode=ParseMode.MARKDOWN)))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
