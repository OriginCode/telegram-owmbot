#!/usr/bin/python

import configparser
import logging
import requests
import json
import pyowm
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import sleep

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

config =  configparser.ConfigParser()
config.read('./config.ini')

owm = pyowm.OWM(API_key=config['BOT']['APPID'])

def weather(update, context):
    city = context.args[0].replace('_', ' ')
    try:
        obs = owm.weather_at_places(city, searchtype='accurate', limit=int(context.args[1]) + 1)
    except IndexError:
        obs = owm.weather_at_places(city, searchtype='accurate', limit=3)
    
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

        update.message.reply_text('[ %s - %s (lon:%.3f lat:%.3f) ]\nWeather: %s\nCurrent Temperature: %d °C\nHumidity: %d%%\nWind Speed: %d m/s\nWind Degree: %d°' % 
            (country, city, lon, lat, weather, temp, humidity, wind_speed, wind_deg))

    sleep(1)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(config['BOT']['TOKEN'], use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("weather", weather, pass_args=True))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
