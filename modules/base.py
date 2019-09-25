import pip
from telegram import ParseMode

__all__ = ['version', 'about', 'ping', 'help']


def version(update, context):
    update.message.reply_text(
        '`PROJEKT WEATHERBOT, RELEASE 20190925a`\n'
        '`python-telegram-bot: %s`\n'
        % __import__('telegram').__version__, parse_mode=ParseMode.MARKDOWN)


def about(update, context):
    update.message.reply_text(
        '*GITHUB*\n'
        'https://github.com/OriginCode/telegram-owmbot',
        parse_mode=ParseMode.MARKDOWN)


def ping(update, context):
    update.message.reply_text('Pong!')


def help(update, context):
    update.message.reply_text(
        '*OriginCode\'s OWM Bot*\n'
        'Made with *LOVE* and *NYAA*\n\n'
        '*COMMANDS*\n'
        'Get OpenWeatherMap weather info: `/owmweather <City>[,Country] [Num of Reqs (Default: 2)]`\n'
        'Get version: `/version`\n'
        'About this bot: `/about`\n'
        'Ping!: `/ping`\n'
        'Display this help message: `/help`\n\n'
        '*AUTHOR*\n'
        '@OriginCode', parse_mode=ParseMode.MARKDOWN)
