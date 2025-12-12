import requests

API_KEY = "6038db8cc579f56543f5ef433a67e254"  # <--- put your API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    # API error?
    if response.status_code != 200:
        return {"error": "City not found or API error!"}

    return response.json()
