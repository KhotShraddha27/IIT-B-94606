from weather.fetch import get_weather
from utils.formatter import format_weather

city = input("Enter city name: ")
weather_data = get_weather(city)

print(format_weather(weather_data))