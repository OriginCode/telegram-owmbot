from telegram import ParseMode

__all__ = ['version', 'about', 'ping']


def version(update, context):
    update.message.reply_text(
        '`LIBOC v18, PROJEKT WEATHERBOT, PRE_RELEASE V2 BETA 1`', parse_mode=ParseMode.MARKDOWN)


def about(update, context):
    update.message.reply_text(
        'GITHUB: https://github.com/OriginCode/telegram-owmbot')


def ping(update, context):
    update.message.reply_text('Pong!')
