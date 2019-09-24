from telegram import ParseMode

__all__ = ['version', 'about', 'ping']


def version(update, context):
    update.message.reply_text(
        '`PROJEKT WEATHERBOT, RELEASE 20190924a`'
        'python-telegram-bot: %s'
        'pyowm: %s'
        % (__import__('telegram').__version__, '2.1.0'), parse_mode=ParseMode.MARKDOWN) # WORKAROUND: pyowm has no __version__ function.


def about(update, context):
    update.message.reply_text(
        'GITHUB: https://github.com/OriginCode/telegram-owmbot')


def ping(update, context):
    update.message.reply_text('Pong!')
