import os
import requests
import json
from datetime import datetime, timedelta, timezone
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

from dotenv import load_dotenv

load_dotenv(verbose=True)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]


def post_message(request):
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    # parser = WebhookHandler(LINE_CHANNEL_SECRET)
    response = requests.get(
        "https://api.openweathermap.org/data/3.0/onecall",
        params={
            "lat": 62.0397,
            "lon": 129.7422,
            "exclude": "current,minutely,daily,alerts",
            "appid": WEATHER_API_KEY,
            "units": "metric",
            "lang": "ja",
        },
    )
    weather_json = json.loads(response.text)
    weather_info = weather_json["hourly"][0]
    YAKT = timezone(timedelta(hours=+9), "YAKT")
    dt_now = datetime.now(YAKT)
    now = dt_now.strftime("%Y/%m/%d %H:%M")
    japanese_weather_list = ["晴れ", "曇り", "雨", "雪"]
    english_weather_list = ["Clear", "Clouds", "Rain", "Snow"]
    weather = weather_info["weather"][0]["main"]
    if weather in english_weather_list:
        weather = japanese_weather_list[english_weather_list.index(weather)]
    temperature = weather_info["temp"]
    feel_like = weather_info["feels_like"]
    humidity = weather_info["humidity"]
    message = f"{now} (YAKT) のヤクーツク\n天気: {weather} \n気温: {temperature}℃\n体感温度: {feel_like}℃\n湿度: {humidity}%"
    line_bot_api.broadcast(TextSendMessage(text=message))
    return ""
