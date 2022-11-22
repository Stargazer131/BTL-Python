from datetime import datetime, time, timedelta

from pytz import timezone
from telegram import Bot, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

import Weather

# data

TOKEN = Weather.data['bot_token']
bot = Bot(token=TOKEN)
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# store data of unique user id

user_database = dict()

# for printing emoji

icon_bank = {
        "weather": {
            "sunny" : "\U00002600",
            "cloudy" : "\U00002601",
            "rainy" : "\U0001F327",
            "thunderstorm" : "\U000026C8",
            "snowy" : "\U00002744",
            "foggy" : "\U0001F32B",
            "rainbow" : "\U0001F308",
            "temperature" : "\U0001F321",
            "wind_speed" : "\U0001F32C",
            "humidity" : "\U0001F4A7",  
        },
        
        "logo" : {
            "day" : "\U0001F307",
            "night" : "\U0001F303",
            "information" : "\U00002139",
            "city" : "\U0001F3D9",
            "yes" : "\U00002705",
            "no" : "\U0000274E",
            "warning" : "\U000026A0",
            "prohibit" : "\U0001F6AB",
            "calendar" : "\U0001F4C5",
            "bot" : "\U0001F916",      
            "question_mark" : "\U00002753"
        }
}

# init user data for user id in the database

def init_user_data(chat_id: int):
    global user_database
    if chat_id not in user_database:
        user_database[chat_id] = {
            "current_weather_data" : None,
            "flag_current_weather" : False,
            "flag_next_7_days" : False,
            "flag_daily_weather" : False,
            "daily_city" : None,
            "daily_timezone" : None,
            "flag_alert_weather" : False,
            "alert_city" : None,
            "alert_timezone" : None
        }

# /start command


def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
   
    reply = (
        f"Hello, Thanks for choosing Weather Bot! {icon_bank['logo']['bot']}\n"
        f"Type /help for more information {icon_bank['logo']['question_mark']}"
    )
    
    context.bot.send_message(chat_id=chat_id, text=reply)


# /help command

        
def help(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id 
    
    answer = (
    f'The following command are available:\n'
    f"/weather Receive current weather in a city {icon_bank['logo']['city']}\n"
    f"/daily Start receiving daily weather update in a city {icon_bank['weather']['rainbow']}\n"
    f"/alert Start receiving alert update for uncomfortable or hazardous weather in a city {icon_bank['logo']['warning']}\n" 
    f"/stop1 Stop receiving daily weather update {icon_bank['logo']['no']}\n"
    f"/stop2 Stop receiving alert weather update {icon_bank['logo']['no']}\n"
    f"/city1 Check for the city you have chosen for daily weather update {icon_bank['logo']['city']}\n"
    f"/city2 Check for the city you have chosen for alert weather update {icon_bank['logo']['city']}"
    )
    
    context.bot.send_message(chat_id=chat_id, text=answer)   


# text handler    


def reply(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    init_user_data(chat_id)
    
    # if the text receive is after the /weather command
    if user_database[chat_id]['flag_current_weather']:
        if not user_database[chat_id]['flag_next_7_days']:
            current_weather(update, context)
        else:
            weather_next_7_days(update, context)
    
    # if the text receive is after the /daily command
    elif user_database[chat_id]['flag_daily_weather']:
        user_input = update.message.text
        if get_daily_weather(user_input, chat_id):
            
            tz = user_database[chat_id]['daily_timezone']
            city_name = user_database[chat_id]['daily_city']
            
            context.job_queue.run_daily(daily_weather_7AM, 
                                        time=time(hour=7, minute=0, tzinfo=timezone(tz)), 
                                        days=(0, 1, 2, 3, 4, 5, 6), 
                                        context=chat_id,
                                        name=f'{chat_id}daily7AM')
            
            context.job_queue.run_daily(daily_weather_9PM, 
                                        time=time(hour=21, minute=0,tzinfo=timezone(tz)), 
                                        days=(0, 1, 2, 3, 4, 5, 6), 
                                        context=chat_id,
                                        name=f'{chat_id}daily9PM')
            
            reply = (
                f"You will be notified for weather update in {city_name} {icon_bank['logo']['information']}\n"
                f"At 07:00 AM -> Receive today weather\n"
                f"At 09:00 PM -> Receive tomorrow weather"
            )
            context.bot.send_message(chat_id=chat_id, text=reply)
        
        else:
            context.bot.send_message(chat_id=chat_id, text=f"Sorry we can't find the weather data for this city {icon_bank['logo']['warning']}")

    # if the text receive is after the /alert command
    elif user_database[chat_id]['flag_alert_weather']:
        user_input = update.message.text
        if get_alert_weather(user_input, chat_id):
            
            tz = user_database[chat_id]['alert_timezone']
            home = timezone(tz)
            local_time = datetime.now(home)
            seconds_till_next_hour = 3600 - (local_time.minute*60 + local_time.second)
            city_name = user_database[chat_id]['alert_city']
            
            context.job_queue.run_repeating(alert_weather, 
                                            interval=3600,
                                            first=seconds_till_next_hour,
                                            context=chat_id,
                                            name=f'{chat_id}alert')
            
            reply = f"You will be alert for uncomfortable or hazardous weather in {city_name} every hour from 06:00 AM to 09:00 PM {icon_bank['logo']['information']}"
            context.bot.send_message(chat_id=chat_id, text=reply)
        
        else:
            context.bot.send_message(chat_id=chat_id, text=f"Sorry we can't find the weather data for this city {icon_bank['logo']['warning']}")
    
    # discard all other text messages
    else:
        context.bot.send_message(chat_id=chat_id, text=f"Sorry we don't support this command! {icon_bank['logo']['prohibit']}\nPlease try again!")


# /alert command


def alert(update: Update, context: CallbackContext):
    global user_database
    chat_id = update.message.chat_id
    init_user_data(chat_id)
    
    user_database[chat_id]['flag_alert_weather'] = True
    context.bot.send_message(chat_id=chat_id, text=f"Please enter the city name {icon_bank['logo']['city']}")


# get alert weather


def get_alert_weather(user_input: str, chat_id: int) -> bool:
    global user_database
    
    try:
        city_name, country, current_weather_data = Weather.get_city_weather(user_input)
        
    except:
        user_database[chat_id]['alert_city'] = None
        return False
    
    else:
        user_database[chat_id]['alert_city'] = f'{city_name}/{country}'
        user_database[chat_id]['alert_timezone'] = current_weather_data['timezone']
        return True

    finally:
        user_database[chat_id]['flag_alert_weather'] = False


# send alert weather information


def alert_weather(context: CallbackContext):
    chat_id = context.job.context
    
    home = timezone(user_database[int(chat_id)]['alert_timezone'])
    local_time = datetime.now(home)
    if local_time.hour >= 22 or local_time.hour <= 5:
        return
    
    city = user_database[int(chat_id)]['alert_city'][:-3]
    city_name, country, current_weather_data = Weather.get_city_weather(city)
    
    next_hour_weather_data = current_weather_data['hourly'][1]
    
    icon_id = next_hour_weather_data['weather'][0]['icon']
    weather_status = Weather.data['weather_condition'][icon_id]
    
    if weather_status in ("rainy", "foggy", "thunderstorm", "snowy"):
        icon = icon_bank['weather'][weather_status]
        weather = next_hour_weather_data['weather'][0]['main']
        weather_description = next_hour_weather_data['weather'][0]['description']
        temperature = next_hour_weather_data['temp']
        wind_speed = next_hour_weather_data['wind_speed']
        humidity = next_hour_weather_data['humidity']

        context.bot.send_message(chat_id=chat_id, 
                                 text=f"ALERT, weather within the next hour in {city_name.title()}/{country} will be {icon_bank['logo']['information']}\n")

        answer = (
            f'The weather is: {weather}, {weather_description}\n'
            f'{icon}\n'
            f"Temperature: {temperature:.0f}°C {icon_bank['weather']['temperature']}\n"
            f"Wind speed: {wind_speed} mps {icon_bank['weather']['wind_speed']}\n"
            f"Humidity: {humidity}% {icon_bank['weather']['humidity']}\n"
            f"Please be careful! {icon_bank['logo']['warning']}"
        )

        context.bot.send_message(chat_id=chat_id, text=answer)
        
    else:
        context.bot.send_message(chat_id=chat_id, text=f"You can expected for weather in {city_name.title()}/{country} will be normal within the next hour {icon_bank['weather']['rainbow']}")


# get alert city name


def get_current_alert_city(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    init_user_data(chat_id)
    
    city = user_database[chat_id]['alert_city']
    if city == None:
        reply = f"You haven't chosen any alert update yet! {icon_bank['logo']['warning']}"
    else:
        reply = f"Your current city for alert weather update is: {city} {icon_bank['logo']['city']}"
    
    bot.send_message(chat_id=chat_id, text=reply)


# stop alert weather command


def stop_alert_update(update: Update, context: CallbackContext):
    global user_database
    
    chat_id = update.message.chat_id
    try:
        job = context.job_queue.get_jobs_by_name(f'{chat_id}alert')
        job[0].schedule_removal()
    except:
        context.bot.send_message(chat_id=chat_id, text=f"You haven't chosen any alert update yet! {icon_bank['logo']['warning']}")
    else:
        context.bot.send_message(chat_id=chat_id, text='Stop receive alert update!')
        user_database[chat_id]['alert_city'] = None
        

# /daily command

def start_daily_update(update: Update, context: CallbackContext):
    global user_database
    chat_id = update.message.chat_id
    init_user_data(chat_id)
    
    user_database[chat_id]['flag_daily_weather'] = True
    context.bot.send_message(chat_id=chat_id, text=f"Please enter the city name {icon_bank['logo']['city']}")


# get daily weather data


def get_daily_weather(user_input: str, chat_id: int) -> bool:
    global user_database
    
    try:
        city_name, country, current_weather_data = Weather.get_city_weather(user_input)
    except:
        user_database[chat_id]['daily_city'] = None
        return False
    else:
        user_database[chat_id]['daily_timezone'] = current_weather_data['timezone']
        user_database[chat_id]['daily_city'] = f'{city_name}/{country}'
        return True
    finally:
        user_database[chat_id]['flag_daily_weather'] = False
                

# send back daily weather at 07:00 AM


def daily_weather_7AM(context: CallbackContext):
    chat_id = context.job.context
    
    city = user_database[int(chat_id)]['daily_city'][:-3]
    city_name, country, today_weather_data = Weather.get_city_weather(city)
    
    home = timezone(user_database[int(chat_id)]['daily_timezone'])
    local_time = datetime.now(home)
    today = local_time.strftime("%a %d")
    
    icon_id = today_weather_data['daily'][0]['weather'][0]['icon']
    weather_status = Weather.data['weather_condition'][icon_id]
    icon = icon_bank['weather'][weather_status]
    
    weather = today_weather_data['daily'][0]['weather'][0]['main']
    weather_description = today_weather_data['daily'][0]['weather'][0]['description']
    day_temperature = today_weather_data['daily'][0]['temp']['day']
    night_temperature = today_weather_data['daily'][0]['temp']['night']
    wind_speed = today_weather_data['daily'][0]['wind_speed']
    humidity = today_weather_data['daily'][0]['humidity']
    
    
    context.bot.send_message(chat_id=chat_id, text=f"Daily weather in {city_name.title()}/{country} {icon_bank['logo']['information']}\n")

    answer = (
        f"{today} {icon_bank['logo']['calendar']}\n"
        f'The weather is: {weather}, {weather_description}\n'
        f'{icon}\n'
        f"{icon_bank['logo']['day']}Day temperature: {day_temperature:.0f}°C {icon_bank['weather']['temperature']}\n"
        f"{icon_bank['logo']['night']}Night temperature: {night_temperature:.0f}°C {icon_bank['weather']['temperature']}\n"
        f"Wind speed: {wind_speed} mps {icon_bank['weather']['wind_speed']}\n"
        f"Humidity: {humidity}% {icon_bank['weather']['humidity']}"
    )

    context.bot.send_message(chat_id=chat_id, text=answer)


# send back tomorrow weather at 09:00 PM


def daily_weather_9PM(context: CallbackContext):
    chat_id = context.job.context
    
    city = user_database[int(chat_id)]['daily_city'][:-3]
    city_name, country, tomorrow_weather_data = Weather.get_city_weather(city)
    
    home = timezone(user_database[int(chat_id)]['daily_timezone'])
    local_time = datetime.now(home)+timedelta(days=1)
    tomorrow = local_time.strftime("%a %d")
    
    icon_id = tomorrow_weather_data['daily'][1]['weather'][0]['icon']
    weather_status = Weather.data['weather_condition'][icon_id]
    icon = icon_bank['weather'][weather_status]
    
    weather = tomorrow_weather_data['daily'][1]['weather'][0]['main']
    weather_description = tomorrow_weather_data['daily'][1]['weather'][0]['description']
    temperature = tomorrow_weather_data['daily'][1]['temp']['day']
    wind_speed = tomorrow_weather_data['daily'][1]['wind_speed']
    humidity = tomorrow_weather_data['daily'][1]['humidity']
    
    
    context.bot.send_message(chat_id=chat_id, text=f"Tomorrow weather in {city_name.title()}/{country} {icon_bank['logo']['information']}\n")

    answer = (
        f"{tomorrow} {icon_bank['logo']['calendar']}\n"
        f"The weather will be: {weather}, {weather_description}\n"
        f"{icon}\n"
        f"Temperature: {temperature:.0f}°C {icon_bank['weather']['temperature']}\n"
        f"Wind speed: {wind_speed} mps {icon_bank['weather']['wind_speed']}\n"
        f"Humidity: {humidity}% {icon_bank['weather']['humidity']}"
    )

    context.bot.send_message(chat_id=chat_id, text=answer)


# /city command


def get_current_daily_city(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    init_user_data(chat_id)
    
    city = user_database[chat_id]['daily_city']
    if city == None:
        reply = f"You haven't chosen any daily update yet! {icon_bank['logo']['warning']}"
    else:
        reply = f"Your current city for daily weather update is: {city} {icon_bank['logo']['city']}"
    
    bot.send_message(chat_id=chat_id, text=reply)


# /stop command


def stop_daily_update(update: Update, context: CallbackContext):
    global user_database
    
    chat_id = update.message.chat_id
    try:
        job1 = context.job_queue.get_jobs_by_name(f'{chat_id}daily7AM')
        job1[0].schedule_removal()
        
        job2 = context.job_queue.get_jobs_by_name(f'{chat_id}daily9PM')
        job2[0].schedule_removal()
    except:
        context.bot.send_message(chat_id=chat_id, text=f"You haven't chosen any daily update yet! {icon_bank['logo']['warning']}")
    else:
        context.bot.send_message(chat_id=chat_id, text='Stop receive daily update!')
        user_database[chat_id]['daily_city'] = None


# /weather command 


def weather(update: Update, context: CallbackContext):
    global user_database
    chat_id = update.message.chat_id
    
    init_user_data(chat_id)
    user_database[chat_id]['flag_current_weather'] = True
    context.bot.send_message(chat_id=chat_id, text=f"Please enter the city name {icon_bank['logo']['city']}")


# display current weather


def current_weather(update: Update, context: CallbackContext):
    global user_database
    chat_id = update.message.chat_id
    city = update.message.text
    
    try:
        city_name, country, current_weather_data = Weather.get_city_weather(city)
    except:
        context.bot.send_message(chat_id=chat_id, text=f"Sorry we can't find the weather data for this city {icon_bank['logo']['prohibit']}")
        user_database[chat_id]['flag_current_weather'] = False
    else:
        user_database[chat_id]['current_weather_data'] = current_weather_data
        
        icon_id = current_weather_data['current']['weather'][0]['icon']
        weather_status = Weather.data['weather_condition'][icon_id]
        icon = icon_bank['weather'][weather_status]
        
        current_weather = current_weather_data['current']['weather'][0]['main']
        current_weather_description = current_weather_data['current']['weather'][0]['description']
        current_temperature = current_weather_data['current']['temp']
        current_feels_like = current_weather_data['current']['feels_like']
        current_wind_speed = current_weather_data['current']['wind_speed']
        current_humidity = current_weather_data['current']['humidity']
    
    
        context.bot.send_message(chat_id=chat_id, text=f"Weather in {city_name.title()}/{country} {icon_bank['logo']['information']}\n")

        answer = (
        f'Current weather is: {current_weather}, {current_weather_description}\n'
        f'{icon}\n'
        f"Temperature: {current_temperature:.0f}°C {icon_bank['weather']['temperature']}\n"
        f"Feels like: {current_feels_like:.0f}°C {icon_bank['weather']['temperature']}\n"
        f"Wind speed: {current_wind_speed} mps {icon_bank['weather']['wind_speed']}\n"
        f"Humidity: {current_humidity}% {icon_bank['weather']['humidity']}"
        )
        
        context.bot.send_message(chat_id=chat_id, text=answer)
        
        reply = (
            f'Do you want to receive weather information for the next 7 days?\n'
            f"Type Y {icon_bank['logo']['yes']} or N {icon_bank['logo']['no']}"
        )
        
        context.bot.send_message(chat_id=chat_id, text=reply)
        user_database[chat_id]['flag_next_7_days'] = True


# display next 7 days weather


def weather_next_7_days(update: Update, context: CallbackContext):
    global user_database
    chat_id = update.message.chat_id
    user_input = update.message.text.upper()
    
    if user_input == 'N':
        bot.send_message(chat_id=chat_id, text="You have chosen not to receive more information!")
    elif user_input == 'Y':
        for i in range(1, 8):
            weather_1_day(update, context, i)
    else:
        bot.send_message(chat_id=chat_id, text=f"Sorry we don't support this command! {icon_bank['logo']['prohibit']}\nPlease try again!")
    
    user_database[chat_id]['flag_current_weather'] = False
    user_database[chat_id]['flag_next_7_days'] = False


# display weather in 1 day


def weather_1_day(update: Update, context: CallbackContext, index: int):
    chat_id = update.message.chat_id
    current_weather_data = user_database[chat_id]['current_weather_data']
    
    home = timezone(current_weather_data['timezone'])
    current_time = datetime.now(home)
    
    icon_id = current_weather_data['daily'][index]['weather'][0]['icon']
    weather_status = Weather.data['weather_condition'][icon_id]
    icon = icon_bank['weather'][weather_status]
    
    today = current_time + timedelta(days=index)
    weather = current_weather_data['daily'][index]['weather'][0]['main']
    weather_description = current_weather_data['daily'][index]['weather'][0]['description']
    day_temperature = current_weather_data['daily'][index]['temp']['day']
    night_temperature = current_weather_data['daily'][index]['temp']['night']
    wind_speed = current_weather_data['daily'][index]['wind_speed']
    humidity = current_weather_data['daily'][index]['humidity']
    
    answer = (
        f"{today.strftime('%a %d')} {icon_bank['logo']['calendar']}\n"
        f'The weather is: {weather}, {weather_description}\n'
        f'{icon}\n'
        f"{icon_bank['logo']['day']} Day temperature: {day_temperature:.0f}°C {icon_bank['weather']['temperature']}\n"
        f"{icon_bank['logo']['night']} Night temperature: {night_temperature:.0f}°C {icon_bank['weather']['temperature']}\n"
        f"Wind speed: {wind_speed} mps {icon_bank['weather']['wind_speed']}\n"
        f"Humidity: {humidity}% {icon_bank['weather']['humidity']}" 
    )
    
    bot.send_message(chat_id=chat_id, text=answer)


def main():    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('weather', weather))
    dp.add_handler(CommandHandler('daily', start_daily_update))
    dp.add_handler(CommandHandler('alert', alert))
    dp.add_handler(CommandHandler('stop1', stop_daily_update, pass_job_queue=True))
    dp.add_handler(CommandHandler('stop2', stop_alert_update, pass_job_queue=True))
    dp.add_handler(CommandHandler('city1', get_current_daily_city))
    dp.add_handler(CommandHandler('city2', get_current_alert_city))
    
    dp.add_handler(MessageHandler(Filters.text, reply, pass_job_queue=True))
    
    updater.start_polling()
    updater.idle()
    

if __name__ == '__main__':    
    main()