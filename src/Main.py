from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk
from pytz import timezone

import Weather

# flag for changing background gif

flip = 0

# main frame

window = Tk()
window.geometry('950x550+250+100')
window.title("Weather Forecast")
window.iconphoto(True, PhotoImage(file = 'images\\app images\\icon.png'))
window.resizable(False, False)

#C and F degrees variable
C_degree = BooleanVar(value = True)
F_degree = BooleanVar(value = False)

# Back_Ground_Gif

Back_Ground_Gif = Label(window)
Back_Ground_Gif.place(x=0, y=0)

# Start of display gif

# Back_Ground_Gif snow

info = Image.open("background\\snowy.gif")
snow_frame_len = info.n_frames
snow_frames = [PhotoImage(file="background\\snowy.gif",
                          format = 'gif -index %i' %(i)) for i in range(snow_frame_len)]


def update_snow(ind, status):
      if flip != status:
            return
      frame = snow_frames[ind]
      ind += 1
      if ind > snow_frame_len - 1: 
         ind = 0
      Back_Ground_Gif.configure(image = frame)
      window.after(40, lambda x: update_snow(ind, status), ind)
    

def display_snow():
      global flip
      flip = flip + 1 % 10
      update_snow(0, flip)


#Back_Ground_Gif fog

info = Image.open("background\\foggy.gif")
fog_frame_len = info.n_frames
fog_frames = [PhotoImage(file="background\\foggy.gif", 
                         format='gif -index %i' %(i)) for i in range(fog_frame_len)]


def update_fog(ind, status):
      if flip != status:
            return
      frame = fog_frames[ind]
      ind += 1
      if ind > fog_frame_len - 1: 
         ind = 0
      Back_Ground_Gif.configure(image = frame)
      window.after(200, lambda x: update_fog(ind, status), ind)
    
    
def display_fog():
      global flip
      flip = flip + 1 % 10
      update_fog(0, flip)


#Back_Ground_Gif thunderstorm

info = Image.open("background\\thunderstorm.gif")
thunderstorm_frame_len = info.n_frames
thunderstorm_frames = [PhotoImage(file="background\\thunderstorm.gif",
                                  format = 'gif -index %i' %(i)) for i in range(thunderstorm_frame_len)]


def update_thunderstorm(ind, status):
      if flip != status:
            return
      frame = thunderstorm_frames[ind]
      ind += 1
      if ind > thunderstorm_frame_len - 1: 
         ind = 0
      Back_Ground_Gif.configure(image = frame)
      window.after(70, lambda x: update_thunderstorm(ind, status), ind)
    
    
def display_thunderstorm():
      global flip
      flip = flip + 1 % 10
      update_thunderstorm(0, flip)

# Back_Ground_Gif rain

info = Image.open("background\\rainy.gif")
rain_frame_len = info.n_frames
rain_frames = [PhotoImage(file="background\\rainy.gif",
                          format = 'gif -index %i' %(i)) for i in range(rain_frame_len)]


def update_rain(ind, status):
      if flip != status:
            return
      frame = rain_frames[ind]
      ind += 1
      if ind > rain_frame_len - 1: 
         ind = 0
      Back_Ground_Gif.configure(image = frame)
      window.after(20, lambda x: update_rain(ind, status), ind)
    

def display_rain():
      global flip 
      flip = flip + 1 % 10
      update_rain(0, flip)

#Back_Ground_Gif cloud

info = Image.open("background\\cloudy.gif")
cloud_frame_len = info.n_frames
cloud_frames = [PhotoImage(file="background\\cloudy.gif",
                           format = 'gif -index %i' %(i)) for i in range(cloud_frame_len)]


def update_cloud(ind, status): 
      if status != flip:
            return
      frame = cloud_frames[ind]
      ind += 1
      if ind > cloud_frame_len - 1: 
         ind = 0
      Back_Ground_Gif.configure(image = frame)
      window.after(50, lambda x: update_cloud(ind, status), ind)
    

def display_cloud():
      global flip 
      flip = flip + 1 % 10
      update_cloud(0, flip)

#Back_Ground_Gif sunny

info = Image.open("background\\sunny.gif")
sunny_frame_len = info.n_frames
sunny_frames = [PhotoImage(file="background\\sunny.gif",
                           format = 'gif -index %i' %(i)) for i in range(sunny_frame_len)]


def update_sunny(ind, status):
      if flip != status:
            return
      frame = sunny_frames[ind]
      ind += 1
      if ind > sunny_frame_len - 1: 
         ind = 0
      Back_Ground_Gif.configure(image = frame)
      window.after(35, lambda x: update_sunny(ind, status), ind)
    

def display_sunny():
      global flip
      flip = flip + 1 % 10
      update_sunny(0, flip)   

# end of display gif

def display_gif(weather_id: str):
      weather_type = Weather.data['weather_condition'][weather_id]
      if weather_type == 'sunny':
            display_sunny()
      elif weather_type == 'cloudy':
            display_cloud() 
      elif weather_type == 'rainy':
            display_rain()
      elif weather_type == 'thunderstorm':
            display_thunderstorm()
      elif weather_type == 'snowy':
            display_snow()
      else:
            display_fog()  


def display_current_location_weather():
      textfield.delete(0,END)
      city_name, country, weather_data = Weather.get_current_location_weather()
      textfield.insert(0,city_name)
      display(city_name, country, weather_data)
            
            
def display_city_weather():
      """
      Display weather information of the given city
      """
      city_name = textfield.get()
      try:
            city_name, country, weather_data = Weather.get_city_weather(city_name)
      except:
            messagebox.showinfo(title='Not found', message="This city data is currently not in the database")
      else:
            display(city_name, country, weather_data)


def resize_image(image: Image, width: int, height: int) -> PhotoImage:
      resized_image = image.resize((width, height))
      return ImageTk.PhotoImage(resized_image)


def display(city_name: str, country: str, weather_data: dict):
      # set background background gif
      
      display_gif(weather_data['current']['weather'][0]['icon'])
      
      # set city name
      
      city.configure(text=f'{city_name.title()}/{country}')
      
      # set current time
      
      home = timezone(weather_data['timezone'])
      local_time = datetime.now(home) # find the current time in the time zone
      current_time = local_time.strftime('%I:%M %p') # format the time
      time.configure(text=current_time)  # display the current time
      
      # set current weather icon and weather status
      
      icon_id = weather_data['current']['weather'][0]['icon']
      current_icon = resize_image(Image.open(f'images\\weather\\{icon_id}@2x.png'), 90, 90)
      current_weather_icon_lbl.configure(image=current_icon)
      current_weather_icon_lbl.image = current_icon
      
      weather_status = weather_data['current']['weather'][0]['main']
      current_weather_status.configure(text=weather_status)
      
      # set current temperature and temperature feel like
      
      temperature = weather_data['current']['temp']
      if(C_degree.get() == True):
            current_temperature.configure(text=f'{temperature:.0f}°C')
      else:
            current_temperature.configure(text=f'{(temperature * 1.8 + 32):.0f}°F')
      
      temperature_feel_like = weather_data['current']['feels_like']
      if(C_degree.get() == True):
            current_temperature_feel_like.configure(text = 'feel like ' + f'{temperature_feel_like:.0f}°C')
      else:
            current_temperature_feel_like.configure(text = 'feel like ' + f'{temperature_feel_like * 1.8 + 32:.0f}°F')
      
      # set current weather description
      
      description = weather_data['current']['weather'][0]['description']
      current_weather_description.configure(text=description)
      
      # set current wind
      
      wind = weather_data['current']['wind_speed']
      current_wind.configure(text=f'{wind:.2f} mps')
      
      # set current humidity
      
      humidity = weather_data['current']['humidity']
      current_humidity.configure(text=f'{humidity}%')  
      
      # set current visibility
      
      visibility = weather_data['current']['visibility']   
      current_visibility.configure(text=f'{visibility}m')
      
      # set current pressure
      
      pressure = weather_data['current']['pressure']
      current_pressure.configure(text=f'{pressure}hPa')
      
      # set information day 1
      
      first_day = local_time + timedelta(days=1)
      day1.configure(text=f"{first_day.strftime('%a %d')}")
      
      icon_id = weather_data['daily'][1]['weather'][0]['icon']
      icon_1st = resize_image(Image.open(f'images\weather\{icon_id}@2x.png'), 70, 70)
      weather_day1.configure(image=icon_1st)
      weather_day1.image = icon_1st
      
      day_temperature = weather_data['daily'][1]['temp']['day']
      night_temperature = weather_data['daily'][1]['temp']['night']
      if(C_degree.get() == True):
            day_temperature_day1.configure(text=f'{day_temperature:.0f}°C')
            night_temperature_day1.configure(text=f'{night_temperature:.0f}°C')
      else:
            day_temperature_day1.configure(text=f'{day_temperature * 1.8 + 32:.0f}°F')
            night_temperature_day1.configure(text=f'{night_temperature * 1.8 + 32:.0f}°F')
      
      weather_status_day1 = weather_data['daily'][1]['weather'][0]['main']
      weather_description_day1.configure(text=weather_status_day1)
      
      # set information day 2
      
      second_day = local_time + timedelta(days=2)
      day2.configure(text=second_day.strftime('%a %d'))
      
      icon_id = weather_data['daily'][2]['weather'][0]['icon']
      icon_2nd = resize_image(Image.open(f'images\weather\{icon_id}@2x.png'), 45, 45)
      weather_day2.configure(image=icon_2nd)
      weather_day2.image = icon_2nd
      
      day_temperature = weather_data['daily'][2]['temp']['day']
      night_temperature = weather_data['daily'][2]['temp']['night']
      if(C_degree.get() == True):
            day_temperature_day2.configure(text=f'{day_temperature:.0f}°C')
            night_temperature_day2.configure(text=f'{night_temperature:.0f}°C')
      else:
            day_temperature_day2.configure(text=f'{day_temperature * 1.8 + 32:.0f}°F')
            night_temperature_day2.configure(text=f'{night_temperature * 1.8 + 32:.0f}°F')
      

      # set information day 3
      
      third_day = local_time + timedelta(days=3)
      day3.configure(text=third_day.strftime('%a %d'))
      
      icon_id = weather_data['daily'][3]['weather'][0]['icon']
      icon_3rd = resize_image(Image.open(f'images\weather\{icon_id}@2x.png'), 45, 45)
      weather_day3.configure(image=icon_3rd)
      weather_day3.image = icon_3rd
      
      day_temperature = weather_data['daily'][3]['temp']['day']
      night_temperature = weather_data['daily'][3]['temp']['night']
      if(C_degree.get() == True):
            day_temperature_day3.configure(text=f'{day_temperature:.0f}°C')
            night_temperature_day3.configure(text=f'{night_temperature:.0f}°C')
      else:
            day_temperature_day3.configure(text=f'{day_temperature * 1.8 + 32:.0f}°F')
            night_temperature_day3.configure(text=f'{night_temperature * 1.8 + 32:.0f}°F')
      
      # set information day 4
      
      fourth_day = local_time + timedelta(days=4)
      day4.configure(text=fourth_day.strftime('%a %d'))
      
      icon_id = weather_data['daily'][4]['weather'][0]['icon']
      icon_4th = resize_image(Image.open(f'images\weather\{icon_id}@2x.png'), 45, 45)
      weather_day4.configure(image=icon_4th)
      weather_day4.image = icon_4th
      
      day_temperature = weather_data['daily'][4]['temp']['day']
      night_temperature = weather_data['daily'][4]['temp']['night']
      if(C_degree.get() == True):
            day_temperature_day4.configure(text=f'{day_temperature:.0f}°C')
            night_temperature_day4.configure(text=f'{night_temperature:.0f}°C')
      else:
            day_temperature_day4.configure(text=f'{day_temperature * 1.8 + 32:.0f}°F')
            night_temperature_day4.configure(text=f'{night_temperature * 1.8 + 32:.0f}°F')
      
      # set information day 5
      
      fifth_day = local_time + timedelta(days=5)
      day5.configure(text=fifth_day.strftime('%a %d'))
      
      icon_id = weather_data['daily'][5]['weather'][0]['icon']
      icon_5th = resize_image(Image.open(f'images\weather\{icon_id}@2x.png'), 45, 45)
      weather_day5.configure(image=icon_5th)
      weather_day5.image = icon_5th
      
      day_temperature = weather_data['daily'][5]['temp']['day']
      night_temperature = weather_data['daily'][5]['temp']['night']
      if(C_degree.get() == True):
            day_temperature_day5.configure(text=f'{day_temperature:.0f}°C')
            night_temperature_day5.configure(text=f'{night_temperature:.0f}°C')
      else:
            day_temperature_day5.configure(text=f'{day_temperature * 1.8 + 32:.0f}°F')
            night_temperature_day5.configure(text=f'{night_temperature * 1.8 + 32:.0f}°F')
      
      # set information day 6
      
      sixth_day = local_time + timedelta(days=6)
      day6.configure(text=sixth_day.strftime('%a %d'))
      
      icon_id = weather_data['daily'][6]['weather'][0]['icon']
      icon_6th = resize_image(Image.open(f'images\weather\{icon_id}@2x.png'), 45, 45)
      weather_day6.configure(image=icon_6th)
      weather_day6.image = icon_6th
      
      day_temperature = weather_data['daily'][6]['temp']['day']
      night_temperature = weather_data['daily'][6]['temp']['night']
      if(C_degree.get() == True):
            day_temperature_day6.configure(text=f'{day_temperature:.0f}°C')
            night_temperature_day6.configure(text=f'{night_temperature:.0f}°C')
      else:
            day_temperature_day6.configure(text=f'{day_temperature * 1.8 + 32:.0f}°F')
            night_temperature_day6.configure(text=f'{night_temperature * 1.8 + 32:.0f}°F')
      
      # set information day 7
      
      seventh_day = local_time + timedelta(days=7)
      day7.configure(text=seventh_day.strftime('%a %d'))

      icon_id = weather_data['daily'][7]['weather'][0]['icon']
      icon_7th = resize_image(Image.open(f'images\weather\{icon_id}@2x.png'), 45, 45)
      weather_day7.configure(image=icon_7th)
      weather_day7.image = icon_7th
      
      day_temperature = weather_data['daily'][7]['temp']['day']
      night_temperature = weather_data['daily'][7]['temp']['night']
      if(C_degree.get() == True):
            day_temperature_day7.configure(text=f'{day_temperature:.0f}°C')
            night_temperature_day7.configure(text=f'{night_temperature:.0f}°C')
      else:
            day_temperature_day7.configure(text=f'{day_temperature * 1.8 + 32:.0f}°F')
            night_temperature_day7.configure(text=f'{night_temperature * 1.8 + 32:.0f}°F')

#Frame hold searchbar, setting button and home button

top_frame = Frame(window, 
                  bg = '#364e70',
                  width = 950,
                  height = 57)
top_frame.pack()

#SearchBar

searchbar = PhotoImage(file = 'images\\app images\\searchbar.png')
Label(top_frame,
      image = searchbar,
      bg = '#364e70').place(x = 300, y = 4)

#HomeButton

home = PhotoImage(file = 'images\\app images\\home.png')
Button(top_frame,
       image = home,
       bg = '#364e70',
       activebackground = '#364e70',
       cursor = 'hand2',
       command=display_current_location_weather).place(x = 5, y = 5)

#Setting_Menu
setting = PhotoImage(file = 'images\\app images\\setting.png')   
Setting_Menu = Menubutton(top_frame,
                         image = setting,
                         bg = '#364e70',
                         relief = RAISED,
                         activebackground = '#364e70',
                         cursor = 'hand2')
Setting_Menu.menu = Menu(Setting_Menu,tearoff = False)

def C_degree_setting_display():
      if(C_degree.get() == True):
            Setting_Menu.menu.entryconfig('C_degree',
                                          state = DISABLED,
                                          activebackground = '#f0f0f0',
                                          activeforeground = '#f0f0f0')
            if(F_degree.get() == True):
                  F_degree.set(value = False)
                  Setting_Menu.menu.entryconfig('F_degree',
                                                state = NORMAL,
                                                activebackground = '#34d2eb',
                                                activeforeground = '#34d2eb')
      display_city_weather()

def F_degree_setting_display():
      if(F_degree.get() == True):
            Setting_Menu.menu.entryconfig('F_degree',
                                          state = DISABLED,
                                          activebackground = '#f0f0f0',
                                          activeforeground = '#f0f0f0')
            if(C_degree.get() == True):
                  C_degree.set(value = False)
                  Setting_Menu.menu.entryconfig('C_degree',
                                                state = NORMAL,
                                                activebackground = '#34d2eb',
                                                activeforeground = '#34d2eb')
      display_city_weather()

C_degree_image = PhotoImage(file = 'images\\app images\\c_degree.png')
F_degree_image = PhotoImage(file = 'images\\app images\\f_degree.png')
Setting_Menu.menu.add_checkbutton(label = 'C_degree',
                                  image = C_degree_image,
                                  variable = C_degree,
                                  onvalue = True,
                                  offvalue = False,
                                  state = DISABLED,
                                  activebackground = '#f0f0f0',
                                  activeforeground = '#f0f0f0',                  
                                  command = C_degree_setting_display)
                              
Setting_Menu.menu.add_separator()

Setting_Menu.menu.add_checkbutton(label = 'F_degree',
                                  image = F_degree_image,
                                  variable = F_degree,
                                  onvalue = True,
                                  offvalue = False,
                                  activebackground = '#34d2eb',
                                  activeforeground = '#34d2eb',
                                  command = F_degree_setting_display)
Setting_Menu.place(x = 899, y = 7)
Setting_Menu['menu'] = Setting_Menu.menu

#SearchButton

search = PhotoImage(file = 'images\\app images\\search.png')
Button(top_frame,
       image = search,
       bg = '#4e6381',
       activebackground= '#4e6381',
       borderwidth = 0,
       cursor = 'hand2',
       command=display_city_weather).place(x = 595,y = 11)

#Entry

textfield = Entry(top_frame,
                  width = 18,
                  font = ('poppins',20,'bold'),
                  fg = 'white',
                  insertbackground = 'white',
                  bg = '#4e6381',
                  border = 0)
textfield.place(x = 317,y = 12)

#information_box

bigger_box = PhotoImage(file = 'images\\app images\\bigger.png')
current_information_box = Label(window,
                                image = bigger_box,
                                bg = '#4e6381',
                                relief = GROOVE)
current_information_box.place(x = 20,y = 110)

#day_1st_box

big_box = PhotoImage(file = 'images\\app images\\big.png')
day_1st_box = Label(window,
                     image = big_box,
                     bg = '#4e6381',
                     relief = GROOVE)
day_1st_box.place(x = 20,y = 390)

#Small Boxes

small_box = PhotoImage(file = 'images\\app images\\small.png')

#day_2nd_box

Label(window,
      image = small_box,
      bg = '#4e6381',
      relief = GROOVE).place(x = 300,y = 405)

#day_3rd_box

Label(window,
      image = small_box,
      bg = '#4e6381',
      relief = GROOVE).place(x = 410 ,y = 405)

#day_4th_box

Label(window,
      image = small_box,
      bg = '#4e6381',
      relief = GROOVE).place(x = 520 ,y = 405)

#day_5th_box

Label(window,
      image = small_box,
      bg = '#4e6381',
      relief = GROOVE).place(x = 630 ,y = 405)

#day_6th_box

Label(window,
      image = small_box,
      bg = '#4e6381',
      relief = GROOVE).place(x = 740 ,y = 405)

#day_7th_box

Label(window,
      image = small_box,
      bg = '#4e6381',
      relief = GROOVE).place(x = 850 ,y = 405)

#Information in Current Information Box

#City label

city = Label(window,
            font = ('Segoe UI',14,'bold'),
            fg = 'white',
            bg = '#364e70')
city.place(x = 35, y = 112)

#Today label

Label(window,
      text = 'Today',
      font = ('Segoe UI',14,'bold'),
      fg = 'white',
      bg = '#364e70').place(x = 35,y = 140)

#Current time label

time = Label(window,
             font = ('Segoe UI',10),
             fg = 'white',
             bg = '#364e70')
time.place(x = 100,y = 145)

#Current weather icon

current_weather_icon_lbl = Label(window,bg = '#364e70')
current_weather_icon_lbl.place(x = 25,y = 175)

# Current temperature and temperature feel like label 

current_temperature = Label(window,
                    font = ('Segoe UI',38,'bold'),
                    bg = '#364e70',
                    fg = 'white')
current_temperature.place(x = 130, y = 190)

current_temperature_feel_like = Label(window,
                       font = ('Segoe UI',13,'bold'),
                       fg = 'white',
                       bg = '#364e70')
current_temperature_feel_like.place(x = 300,y = 195)

# current weather description label

current_weather_description = Label(window,
                            font = ('Segoe UI',13,'bold'),
                            bg = '#364e70',
                            fg = 'white',
                            width = 27)
current_weather_description.place(x = 170, y = 140)

# Current weather_status label

current_weather_status = Label(window,
                       font = ('Segoe UI',20,'bold'),
                       fg = 'white',
                       bg = '#364e70')
current_weather_status.place(x = 300,y = 220)

# Current wind label

Label(window,
      text = 'WIND',
      font = ('Segoe UI',11),
      bg = '#364e70',
      fg = 'white').place(x = 35,y = 280)


current_wind = Label(window,
             font = ('Segoe UI',11),
             bg = '#364e70',
             fg = 'white')
current_wind.place(x = 35,y = 300)

# Current humidity label

Label(window,
      text = 'HUMIDITY',
      font = ('Segoe UI',11),
      bg = '#364e70',
      fg = 'white').place(x = 135,y = 280)


current_humidity = Label(window,
                 font = ('Segoe UI',11),
                 bg = '#364e70',
                 fg = 'white')
current_humidity.place(x = 135,y = 300)

# Current visibility label

Label(window,
      text = 'VISIBILITY',
      font = ('Segoe UI',11),
      bg = '#364e70',
      fg = 'white').place(x = 235,y = 280)


current_visibility = Label(window,
                   font = ('Segoe UI',11),
                   bg = '#364e70',
                   fg = 'white')
current_visibility.place(x = 235,y = 300)

# Current pressure label

Label(window,
      text = 'PRESSURE',
      font = ('Segoe UI',11),
      bg = '#364e70',
      fg = 'white').place(x = 335,y = 280)


current_pressure = Label(window,
                 font = ('Segoe UI',11),
                 bg = '#364e70',
                 fg = 'white')
current_pressure.place(x = 335,y = 300)

#Information_in_1st_day_box

# day in week and day in month of day1

day1 = Label(window,
             font = ('Segoe UI',12),
             bg = '#364e70',
             fg = 'white')
day1.place(x = 35,y = 400)

# weather icon day1

weather_day1 = Label(window,bg = '#364e70')
weather_day1.place(x = 25,y = 425)

# day temperature day1

day_temperature_day1 = Label(window,
                             font = ('Segoe UI',12),
                             bg = '#364e70',
                             fg = 'white')
day_temperature_day1.place(x = 100,y = 435)

# night temperature day1

night_temperature_day1 = Label(window,
                               font = ('Segoe UI',12),
                               bg = '#364e70',
                               fg = 'white')
night_temperature_day1.place(x = 100,y = 465)

# weather description day1

weather_description_day1 = Label(window,
                                 font = ('Segoe UI',15),
                                 bg = '#364e70',
                                 fg = 'white')
weather_description_day1.place(x = 180,y = 445)

#Information_in_2nd -> 7th_day_box

# day 2

# day in week and day in month of day2

day2 = Label(window,
            font = ('Segoe UI',10),
            bg = '#364e70',
            fg = 'white',
            width = 9)
day2.place(x = 306,y = 410)

# weather icon day2

weather_day2 = Label(window,bg = '#364e70')
weather_day2.place(x = 316,y = 430)

# day temperature day2

day_temperature_day2 = Label(window,
                             font = ('Segoe UI', 10),
                             bg = '#364e70',
                             fg = 'white',
                             width = 9)
day_temperature_day2.place(x = 307,y = 485)

# night temperature day2

night_temperature_day2 = Label(window,
                             font = ('Segoe UI', 10),
                             bg = '#364e70',
                             fg = 'white',
                             width = 9)
night_temperature_day2.place(x = 307,y = 505)

# day 3

# day in week and day in month of day3

day3 = Label(window,
             font = ('Segoe UI',10),
             bg = '#364e70',
             fg = 'white',
             width = 9)
day3.place(x = 416,y = 410)

# weather icon day3

weather_day3 = Label(window,bg = '#364e70')
weather_day3.place(x = 426,y = 430)

# day temperature day3

day_temperature_day3 = Label(window,
                             font = ('Segoe UI', 10),
                             bg = '#364e70',
                             fg = 'white',
                             width = 9)
day_temperature_day3.place(x = 417,y = 485)

# night temperature day3

night_temperature_day3 = Label(window,
                             font = ('Segoe UI', 10),
                             bg = '#364e70',
                             fg = 'white',
                             width = 9)
night_temperature_day3.place(x = 417,y = 505)

# day 4

# day in week and day in month of day4

day4 = Label(window,
             font = ('Segoe UI',10),
             bg = '#364e70',
             fg = 'white',
             width = 9)
day4.place(x = 526,y = 410)

# weather icon day4

weather_day4 = Label(window,bg = '#364e70')
weather_day4.place(x = 536,y = 430)

# day temperature day4

day_temperature_day4 = Label(window,
                             font = ('Segoe UI', 10),
                             bg = '#364e70',
                             fg = 'white',
                             width = 9)
day_temperature_day4.place(x = 527,y = 485)

# night temperature day4

night_temperature_day4 = Label(window,
                             font = ('Segoe UI', 10),
                             bg = '#364e70',
                             fg = 'white',
                             width = 9)
night_temperature_day4.place(x = 527,y = 505)

# day 5

# day in week and day in month of day5

day5 = Label(window,
             font = ('Segoe UI',10),
             bg = '#364e70',
             fg = 'white',
             width = 9)
day5.place(x = 636,y = 410)

# weather icon day5

weather_day5 = Label(window,bg = '#364e70')
weather_day5.place(x = 646,y = 430)

# day temperature day5

day_temperature_day5 = Label(window,
                             font = ('Segoe UI', 10),
                             bg = '#364e70',
                             fg = 'white',
                             width = 9)
day_temperature_day5.place(x = 637,y = 485)

# night temperature day5

night_temperature_day5 = Label(window,
                             font = ('Segoe UI', 10),
                             bg = '#364e70',
                             fg = 'white',
                             width = 9)
night_temperature_day5.place(x = 637,y = 505)

# day 6

# day in week and day in month of day6

day6 = Label(window,
             font = ('Segoe UI',10),
             bg = '#364e70',
             fg = 'white',
             width = 9)
day6.place(x = 746,y = 410)

# weather icon day6

weather_day6 = Label(window,bg = '#364e70')
weather_day6.place(x = 756,y = 430)

# day temperature day6

day_temperature_day6 = Label(window,
                             font = ('Segoe UI', 10),
                             bg = '#364e70',
                             fg = 'white',
                             width = 9)
day_temperature_day6.place(x = 747,y = 485)

# night temperature day6

night_temperature_day6 = Label(window,
                             font = ('Segoe UI', 10),
                             bg = '#364e70',
                             fg = 'white',
                             width = 9)
night_temperature_day6.place(x = 747,y = 505)

# day 7

# day in week and day in month of day7

day7 = Label(window,
             font = ('Segoe UI',10),
             bg = '#364e70',
             fg = 'white',
             width = 9)
day7.place(x = 856,y = 410)

# weather icon day7

weather_day7 = Label(window,bg = '#364e70')
weather_day7.place(x = 866,y = 430)

# day temperature day7

day_temperature_day7 = Label(window,
                             font = ('Segoe UI', 10),
                             bg = '#364e70',
                             fg = 'white',
                             width = 9)
day_temperature_day7.place(x = 857,y = 485)

# night temperature day7

night_temperature_day7 = Label(window,
                             font = ('Segoe UI', 10),
                             bg = '#364e70',
                             fg = 'white',
                             width = 9)
night_temperature_day7.place(x = 857,y = 505)

# when hit enter

window.bind('<Return>', lambda event: display_city_weather())

# by default, display the current location weather

display_current_location_weather()
window.mainloop()