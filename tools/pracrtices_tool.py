"""import requests
import json
from langchain_core.tools import tool
@tool
def weather_tool(city_name:str):
    API_key = "6467f4be3e4faf1d1df16a78ff3cd894"
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}"
    responces=requests.get(api)
    output_answer=responces.json()
    locations=output_answer["coord"]
    #loca=output_answer.get("coords")
    weather_out=output_answer["weather"][0]
    tempreture=output_answer["main"]
    country=output_answer["sys"]
    #=country=output_answer["work"][0]
    
    #location=output_answer["result"][0]
    return {
        "latitude": locations["lat"],
        "longitude": locations["lon"],
        "weather_description":weather_out["description"],
        "tempreture":tempreture["temp"],
        "humidity":tempreture["humidity"],
        "country":country["country"],
        "cityname":city_name

    }
input_output=input("Enter the city name:")
output_call=weather_tool.invoke({
    "message":input_output
})
print(output_call)

import requests

def get_historical_weather(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str
):

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_mean,temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)

    data = response.json()

    return data["daily"]
location = get_location("Delhi")

history = get_historical_weather(
    location["latitude"],
    location["longitude"],
    "2026-08-01",
    "2026-08-07"
)

print(history) """