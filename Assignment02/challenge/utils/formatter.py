def format_weather(data):
    if "error" in data:
        return data["error"]

    city = data["name"]
    temp = data["main"]["temp"]
    condition = data["weather"][0]["description"].title()

    return f"Weather in {city}:\nTemperature: {temp}°C\nCondition: {condition}"
