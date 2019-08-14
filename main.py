#!/usr/bin/python

import configparser
import logging
import requests
import json
import pyowm
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import sleep

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('./config.ini')


def __deghandler__(deg):
    if 330 <= deg <= 360 or 0 <= deg < 30:
        return "N"

    elif 30 <= deg < 60:
        return "NE"

    elif 60 <= deg < 120:
        return "E"

    elif 120 <= deg < 150:
        return "SE"

    elif 150 <= deg < 210:
        return "S"

    elif 210 <= deg < 240:
        return "SW"

    elif 240 <= deg < 300:
        return "W"

    elif 300 <= deg < 330:
        return "NW"


class cmd():
    def __init__(self, owmcfg):
        self.owmcfg = owmcfg

    def owmhandler(self, update, context):
        owm = pyowm.OWM(API_key=self.owmcfg['APPID'])
        city = ""
        for i in context.args:
            if not i.isdigit():
                city += i
                city += " "
        city = city[:len(city) - 1]

        if context.args[len(context.args) - 1].isdigit():
            lim = int(context.args[len(context.args) - 1])
            obs = owm.weather_at_places(city, searchtype='accurate', limit=lim)
        else:
            obs = owm.weather_at_places(city, searchtype='accurate', limit=3)

        if len(obs) == 0 or city == "":
            update.message.reply_text(
                '*Invalid City Name!*', parse_mode=ParseMode.MARKDOWN)

        for i in range(len(obs)):
            w = obs[i].get_weather()
            l = obs[i].get_location()

            country = l.get_country()
            city = l.get_name()
            lon = l.get_lon()
            lat = l.get_lat()
            weather = w.get_status()
            temp = w.get_temperature(unit='celsius')['temp']
            humidity = w.get_humidity()
            wind_speed = w.get_wind()['speed']
            wind_deg = w.get_wind()['deg']

            update.message.reply_text(
                '\[ %s - _%s_ (lon:%.3f lat:%.3f) ]\n'
                '*Weather* %s\n'
                '*Current Temperature* %d °C\n'
                '*Humidity* %d%%\n'
                '*Wind Speed* %d m/s\n'
                '*Wind Degree* %s %d°'
                % (country, city, lon, lat, weather, temp, humidity, wind_speed, __deghandler__(wind_deg), wind_deg),
                parse_mode=ParseMode.MARKDOWN)


def version(update, context):
    update.message.reply_text(
        '`LIBOC v18, PROJEKT WEATHERBOT, PRE_RELEASE V2 BETA 1`', parse_mode=ParseMode.MARKDOWN)


def about(update, context):
    update.message.reply_text(
        'GITHUB: https://github.com/OriginCode/telegram-owmbot')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(config['BOT']['TOKEN'], use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('weather', cmd(config['OWM']).owmhandler,
                                  pass_args=True))
    dp.add_handler(CommandHandler('version', version, pass_args=False))
    dp.add_handler(CommandHandler('about', about, pass_args=False))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
