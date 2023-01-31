import tweepy
import os
import requests
import json
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

load_dotenv(verbose=True)

API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]


def post_tweet(request):

    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )
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
    post_request = client.create_tweet(text=message)
    return post_request.data
