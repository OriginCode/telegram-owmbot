#!/usr/bin/python

import configparser
import logging
import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import sleep

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

config =  configparse.ConfigParser()
config.read('./config.ini')

def weather(update, context):
    city = context.args[0]
    city_id = 0
    if len(context.args) > 1:
        for i in range(1, len(context.args)):
            city = city + " " + context.args[i]
    with open('./city.list.json') as f:
        l = json.load(f)
        for i in l:
            if i['name'] == city:
                city_id = i['id']
                break
            else:
                continue
    req = requests.get('http://api.openweathermap.org/data/2.5/weather?id=%s&APPID=%s&units=metric' % (city_id, config['BOT']['APPID'])).json()
    country = req['sys']['country']
    city = req['name']
    weather = req['weather'][0]['main']
    temp = req['main']['temp']
    wind_speed = req['wind']['speed']
    update.message.reply_text('[ %s - %s ] Weather: %s, Current Temperature: %d °C, Wind Speed: %s m/s.' % 
            (country, city, weather, temp, wind_speed))
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
