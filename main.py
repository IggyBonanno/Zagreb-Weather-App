import tkinter as tk
import requests
from PIL import ImageTk, Image

def get_weather():
    city = "Zagreb"
    api_key = "b89161cfb460703f1ced613fa93a7180"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        weather = {
            "description": weather_data["weather"][0]["description"],
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "pressure": weather_data["main"]["pressure"],
            "icon": weather_data["weather"][0]["icon"]
        }
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        weather = None
    return weather

def show_weather():
    weather = get_weather()
    if weather:
        description_label.config(text=weather["description"])
        temperature_label.config(text=f"{weather['temperature']}°C")
        humidity_label.config(text=f"Humidity: {weather['humidity']}%")
        pressure_label.config(text=f"Pressure: {weather['pressure']} hPa")
        icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}.png"
        try:
            response = requests.get(icon_url, stream=True)
            response.raise_for_status()
            response.raw.decode_content = True
            img = Image.open(response.raw).resize((100, 100))
            icon = ImageTk.PhotoImage(img)
            icon_label.config(image=icon)
            icon_label.image = icon
        except requests.exceptions.RequestException as e:
            print("Error:", e)

root = tk.Tk()
root.title("Weather App-Zagreb-IT©2023")
root.geometry("340x340")
root.resizable(False, False)

# Load the background image
bg_image = Image.open("C:/Users/iggy/Desktop/zagreb.jpg")
bg_image = bg_image.resize((340, 340), Image.ANTIALIAS)  # resize the image to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label for the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

description_label = tk.Label(root, text="", font=("Arial", 20))
description_label.pack()

icon_label = tk.Label(root)
icon_label.pack()

temperature_label = tk.Label(root, text="", font=("Arial", 16))
temperature_label.pack()

humidity_label = tk.Label(root, text="", font=("Arial", 12))
humidity_label.pack()

pressure_label = tk.Label(root, text="", font=("Arial", 12))
pressure_label.pack()

search_button = tk.Button(root, text="Refresh", command=show_weather)
search_button.pack()

show_weather()

root.mainloop()
