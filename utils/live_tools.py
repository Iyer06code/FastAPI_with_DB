import requests

def get_weather(city):
    API_KEY = "YOUR_WEATHER_KEY"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    data = res.json()

    if res.status_code != 200:
        return "Weather data not found."

    return f"""
Weather in {data['name']}:
Temperature: {data['main']['temp']}°C
Condition: {data['weather'][0]['description']}
Humidity: {data['main']['humidity']}%
"""
