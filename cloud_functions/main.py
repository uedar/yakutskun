import tweepy
import os
import requests
import json
from datetime import datetime, timedelta, timezone

# from dotenv import load_dotenv

# load_dotenv(verbose=True)
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
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": "yakutsk",
            "appid": WEATHER_API_KEY,
            "units": "metric",
            "lang": "ja",
        },
    )
    JST = timezone(timedelta(hours=+9), "JST")
    dt_now = datetime.now(JST)
    now = dt_now.strftime("%Y/%m/%d %H:%M:%S")
    response_text = json.loads(response.text)
    weather = response_text["weather"][0]["description"]
    temp = response_text["main"]["temp"]
    humidity = response_text["main"]["humidity"]
    message = f"{now}現在のヤクーツク\n天気: {weather} \n気温: {temp}℃\n湿度: {humidity}%"
    client.create_tweet(text=message)
    return ""
