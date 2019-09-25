import pip
from telegram import ParseMode

__all__ = ['version', 'about', 'ping']


def version(update, context):
    update.message.reply_text(
        '`PROJEKT WEATHERBOT, RELEASE 20190924a`\n'
        '`python-telegram-bot: %s`\n'
        '`pyowm: %s`'
        % (__import__('telegram').__version__, __import__('os').system('pip freeze | grep "pyowm"').split('==')[1]), parse_mode=ParseMode.MARKDOWN) # WORKAROUND: pyowm has no __version__ function.


def about(update, context):
    update.message.reply_text(
        'GITHUB: https://github.com/OriginCode/telegram-owmbot')


def ping(update, context):
    update.message.reply_text('Pong!')
