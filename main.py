import COVID19Py
import telebot
from telebot import types
import country
import flag
import requests

covid19 = COVID19Py.COVID19()
bot = telebot.TeleBot("TOKEN")
url = 'https://coronavirus-tracker-api.herokuapp.com/v2/locations'

@bot.message_handler(commands=['start'])
def start(message):
    country_code = country.all_country()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton('🦠 Во всём мире'))

    for c_code in country_code:
        markup.add(types.InlineKeyboardButton(str(c_code['name']).title()))

    send_mess = "<b>Привет " + message.from_user.first_name + "! </b> \nВведите страну"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def mess(message):
    final_message = ""
    get_message_bot = message.text.strip().lower()
    country_code = country.get_county_name(get_message_bot)
    if country_code:
        try:
            resp = requests.get(url=url+'?country_code=' + country_code)
            if 'detail' in resp.json():
                final_message = "<u>" + resp.json()['detail'] + "</u>"
            else:
                location = resp.json()
            # location = covid19.getLocationByCountryCode(country_code)
        except requests.HTTPError:
            pass
    else:
        resp = requests.get(url=url)
        location = resp.json()['latest']
        final_message = "<u>Даннык по всему миру:</u>\n<b>Заболевшие:</b> " + str(
            location['confirmed']) + "\n<b>Число погибших: </b>" + str(location['deaths'])

    if final_message == "":
        date = location['locations'][0]['last_updated'].split('T')
        time = date[1].split('.')
        final_message = "<u>Данные по стране:</u>\nНаселения: " + str(location['locations'][0]['country_population']) + "\n<b>Последние обновления:</b>\n" + str(date[0]) + " " + str(time[0]) + "\n<b>Число заболевших:</b> " + str(location['locations'][0]['latest']['confirmed']) + "\n<b>Число погибших:</b> " + str(location['locations'][0]['latest']['deaths']) + "\n<b>Выздоровление:</b> " + str(location['locations'][0]['latest']['recovered'])

    bot.send_message(message.chat.id, final_message, parse_mode='html')

bot.polling(none_stop=True)


