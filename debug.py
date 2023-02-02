import os
import requests
import json
from datetime import datetime, timedelta, timezone
import base64, hashlib, hmac
from flask import abort, jsonify
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from dotenv import load_dotenv

load_dotenv(verbose=True)

WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
YAKT = timezone(timedelta(hours=+9), "YAKT")
dt_now = datetime.now(YAKT)
dt = dt_now + timedelta(-1)
dt_str = dt.strftime("%Y/%m/%d")
print(dt)
unix_dt = int(dt.timestamp())
print(unix_dt)
response = requests.get(
    "https://api.openweathermap.org/data/3.0/onecall/timemachine",
    params={
        "lat": 62.0397,
        "lon": 129.7422,
        "dt": unix_dt,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ja",
    },
)
weather_json = json.loads(response.text)
print(weather_json)
weather_info = weather_json["data"][0]
japanese_weather_list = ["晴れ", "曇り", "雨", "雪"]
english_weather_list = ["Clear", "Clouds", "Rain", "Snow"]
weather = weather_info["weather"][0]["main"]
if weather in english_weather_list:
    weather = japanese_weather_list[english_weather_list.index(weather)]
temperature = weather_info["temp"]
feel_like = weather_info["feels_like"]
humidity = weather_info["humidity"]
message = f"{dt_str} (YAKT) のヤクーツク\n天気: {weather} \n気温: {temperature}℃\n体感温度: {feel_like}℃\n湿度: {humidity}%"
print(message)
