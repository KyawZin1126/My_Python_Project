from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta

import pytz
import requests
from geopy.geocoders import Nominatim
from PIL import Image, ImageTk
from timezonefinder import TimezoneFinder

root = tk.Tk()
root.title("Weather App")
root.geometry("750x470+300+200")
root.resizable(False,False)
root.configure(bg="#202731")

def getweather():
    city = textfield.get()
    geolocator = Nominatim(user_agent="new")
    location = geolocator.geocode(city)
    obj=TimezoneFinder()
    result = obj.timezone_at(lat = location.latitude, lng = location.longitude)
    timezone.config(text=result)

    long_lat.config(text=f"{round(location.latitude,4)}°N {round(location.longitude,4)}°E")

    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M:%p")
    clock.config(text=current_time)

    api_key = "1921ac6bad0a5d9d7f7bf10e955cccdc"
    api = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    json_data = requests.get(api).json()

    # Current Weather First Forcast
    current = json_data['list'][0]
    temp=current['main']['temp']
    humidity=current['main']['humidity']
    pressure=current['main']['pressure']
    wind_speed=current['wind']['speed']
    description=current['weather'][0]['description']

    t.config(text=f"{temp}°C")
    h.config(text=f"{humidity}%")
    p.config(text=f"{pressure} hPa")
    w.config(text=f"{wind_speed} m/s")
    d.config(text=f"{description}")
    
    # Daily Forcast
    daily_data = []
    for entry in json_data['list']:
        if "12:00:00" in entry['dt_txt']:
            daily_data.append(entry)

    
    icons = []
    temps = []

    for i in range(5):
        if i >= len(daily_data):
            break
        icon_code = daily_data[i]['weather'][0]['icon']
        img = Image.open(f"icon/{icon_code}@2x.png").resize((50,50))
        icons.append(ImageTk.PhotoImage(img))
        temps.append((daily_data[i]['main']['temp_max'],daily_data[i]['main']['feels_like']))


    day_widget = [
        (firstimage,day1,day1temp),
        (secondimage,day2,day2temp),
        (thirdimage,day3,day3temp),
        (fourthimage,day4,day4temp),
        (fifthimage,day5,day5temp)
    ]

    for i, (img_label,day_label,temp_label) in enumerate(day_widget):
        if i >= len(icons):
            break
        img_label.config(image=icons[i])
        img_label.image = icons[i]
        temp_label.config(text=f"Day: {temps[i][0]}\n Night: {temps[i][1]}")
        future_date = datetime.now() + timedelta(days=i+1)
        day_label.config(text=future_date.strftime("%A"))

## Icon
image_icon = PhotoImage(file="Images/Logo.png")
root.iconphoto(False, image_icon)

round_box = PhotoImage(file="Images/Rounded Rectangle 1.png")
Label(root, image=round_box, bg="#202731").place(x=30,y=60)

# Label
Label1 = Label(root, text="Temperature", font=("Segoe UI", 11),fg="#323661", bg="#aad1c8")
Label1.place(x=50,y=120)

Label2 = Label(root, text="Humidity", font=("Segoe UI", 11),fg="#323661", bg="#aad1c8")
Label2.place(x=50,y=140)

Label3 = Label(root, text="Pressure", font=("Segoe UI", 11),fg="#323661", bg="#aad1c8")
Label3.place(x=50,y=160)

Label4 = Label(root, text="Wind Speed", font=("Segoe UI", 11),fg="#323661", bg="#aad1c8")
Label4.place(x=50,y=180)

Label5 = Label(root, text="Description", font=("Segoe UI", 11),fg="#323661", bg="#aad1c8")
Label5.place(x=50,y=200)

# Search Box
search_image = PhotoImage(file="Images/Rounded Rectangle 3.png")
myimage = Label(root, image=search_image, bg="#202731")
myimage.place(x=270, y=122)

weat_img = PhotoImage(file="Images/Layer 7.png")
weatherImage = Label(root, image=weat_img, bg="#333c4c")
weatherImage.place(x=290, y=127)

textfield = tk.Entry(root, justify="center", width=15, font=("Segoe UI", 20, "bold"), border=0, bg="#333c4c", fg="White")
textfield.place(x=370, y=130)

search_icon = PhotoImage(file="Images/Layer 6.png")
myimage_icon = Button (root, image=search_icon, borderwidth=0, cursor="hand2", bg="#333c4c", command=getweather)
myimage_icon.place(x=640, y=135)

# Bottom Box
frame = Frame(root, width=900, height=180, bg="#7094d4")
frame.pack(side=BOTTOM)

# Boxes
firstbox = PhotoImage(file="Images/Rounded Rectangle 2.png")
secondbox = PhotoImage(file="Images/Rounded Rectangle 2 copy.png")

Label(frame, image=firstbox, bg="#7094d4").place(x=30, y=20)
Label(frame, image=secondbox, bg="#7094d4").place(x=300, y=30)
Label(frame, image=secondbox, bg="#7094d4").place(x=400, y=30)
Label(frame, image=secondbox, bg="#7094d4").place(x=500, y=30)
Label(frame, image=secondbox, bg="#7094d4").place(x=600, y=30)

# Clock
clock = Label(root, font=("Segoe UI", 20), bg="#202731", fg="White")
clock.place(x=30, y=20)

# Timezone
timezone = Label(root, font=("Segoe UI", 20), bg="#202731", fg="White")
timezone.place(x=500, y=20)

long_lat = Label(root, font=("Segoe UI", 10), bg="#202731", fg="White")
long_lat.place(x=500, y=60)

# thpwd
t=Label(root, font=("Segoe UI", 9), bg="#333c4c", fg="White")
t.place(x=150, y=120)

h=Label(root, font=("Segoe UI", 9), bg="#333c4c", fg="White")
h.place(x=150, y=140)

p=Label(root, font=("Segoe UI", 9), bg="#333c4c", fg="White")
p.place(x=150, y=160)

w=Label(root, font=("Segoe UI", 9), bg="#333c4c", fg="White")
w.place(x=150, y=180)

d=Label(root, font=("Segoe UI", 9), bg="#333c4c", fg="White")
d.place(x=150, y=200)

# first cell
firstframe = Frame(root, width=230, height=132, bg="#323661")
firstframe.place(x=35, y=315)

firstimage = Label(firstframe, bg="#323661")
firstimage.place(x=1, y=15)

day1 = Label(firstframe, font=("arial 20"), bg="#323661", fg="White")
day1.place(x=70, y=5)

day1temp = Label(firstframe, font=("arial 15 bold"), bg="#323661", fg="White")
day1temp.place(x=10, y=50)

# second cell
secondframe = Frame(root, width=70, height=115, bg="#eeefea")
secondframe.place(x=305, y=325)

secondimage = Label(secondframe, bg="#eeefea")
secondimage.place(x=7, y=20)

day2 = Label(secondframe, font=("arial 10"), bg="#eeefea", fg="#000")
day2.place(x=10, y=5)

day2temp = Label(secondframe, font=("arial 10 bold"), bg="#eeefea", fg="#000")
day2temp.place(x=2, y=70)

# third cell
thirdframe = Frame(root, width=70, height=115, bg="#eeefea")
thirdframe.place(x=405, y=325)

thirdimage = Label(thirdframe, bg="#eeefea")
thirdimage.place(x=7, y=20)

day3 = Label(thirdframe, font=("arial 10"), bg="#eeefea", fg="#000")
day3.place(x=10, y=5)

day3temp = Label(thirdframe, font=("arial 10 bold"), bg="#eeefea", fg="#000")
day3temp.place(x=2, y=70)

# fourth cell
fourthframe = Frame(root, width=70, height=115, bg="#eeefea")
fourthframe.place(x=505, y=325)

fourthimage = Label(fourthframe, bg="#eeefea")
fourthimage.place(x=7, y=20)

day4 = Label(fourthframe, font=("arial 10"), bg="#eeefea", fg="#000")
day4.place(x=10, y=5)

day4temp = Label(fourthframe, font=("arial 10 bold"), bg="#eeefea", fg="#000")
day4temp.place(x=2, y=70)

# fifth cell
fifthframe = Frame(root, width=70, height=115, bg="#eeefea")
fifthframe.place(x=605, y=325)

fifthimage = Label(fifthframe, bg="#eeefea")
fifthimage.place(x=7, y=20)

day5 = Label(fifthframe, font=("arial 10"), bg="#eeefea", fg="#000")
day5.place(x=10, y=5)

day5temp = Label(fifthframe, font=("arial 10 bold"), bg="#eeefea", fg="#000")
day5temp.place(x=2, y=70)






















root.mainloop()