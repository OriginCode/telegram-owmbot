from pyowm import OWM
import configparser
from telegram import ParseMode
from modules.deghandler import __deghandler__

__all__ = ['owmweather']

config = configparser.ConfigParser()
config.read('../config.ini')

def owmweather(update, context):
    owm = OWM(API_key=config['OWM']['APPID'])
    city = ""
    for i in context.args:
        if not i.isdigit():
            city += i
            city += " "
    city = city[:len(city) - 1]

    if context.args[len(context.args) - 1].isdigit():
        lim = int(context.args[len(context.args) - 1])
        obs = owm.weather_at_places(
            city, searchtype='accurate', limit=lim + 1)
    else:
        obs = owm.weather_at_places(city, searchtype='accurate', limit=3)

    if len(obs) == 0:
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
