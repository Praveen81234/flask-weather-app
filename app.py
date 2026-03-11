from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

API_KEY = "d79645663b6a99b2239a710f4d4ea354"

@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    error = None

    if request.method == 'POST':
        city = request.form['city']

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if data.get("cod") == 200:
                # Get weather icon emoji
                icon_code = data["weather"][0]["icon"]
                weather_id = data["weather"][0]["id"]
                
                # Map weather conditions to emojis
                if weather_id < 300:
                    emoji = "⛈️"
                elif weather_id < 400:
                    emoji = "🌧️"
                elif weather_id < 600:
                    emoji = "🌧️"
                elif weather_id < 700:
                    emoji = "❄️"
                elif weather_id < 800:
                    emoji = "🌫️"
                elif weather_id == 800:
                    emoji = "☀️" if "d" in icon_code else "🌙"
                else:
                    emoji = "☁️"
                
                # Get city's local time using timezone offset
                timezone_offset = data["timezone"]  # offset in seconds
                utc_now = datetime.utcnow()
                city_time = utc_now + timedelta(seconds=timezone_offset)
                time_str = city_time.strftime("%I:%M %p")
                date_str = city_time.strftime("%A, %B %d")
                
                weather = {
                    "city": data["name"],
                    "temp": round(data["main"]["temp"]),
                    "desc": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "emoji": emoji,
                    "humidity": data["main"]["humidity"],
                    "wind": round(data["wind"]["speed"] * 3.6),
                    "feels_like": round(data["main"]["feels_like"]),
                    "time": time_str,
                    "date": date_str
                }
            else:
                error = "City not found. Please try again."
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)