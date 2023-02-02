import os
import requests
import json
from datetime import datetime, timedelta, timezone
import base64, hashlib, hmac
from flask import abort, jsonify
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


# from dotenv import load_dotenv

# load_dotenv(verbose=True)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]


def reply_message(request):
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    parser = WebhookParser(LINE_CHANNEL_SECRET)
    body = request.get_data(as_text=True)
    hash = hmac.new(
        LINE_CHANNEL_SECRET.encode("utf-8"), body.encode("utf-8"), hashlib.sha256
    ).digest()
    signature = base64.b64encode(hash).decode()

    if signature != request.headers["X_LINE_SIGNATURE"]:
        return abort(405)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return abort(405)
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        reply_list = ["昨日", "今日", "明日"]
        user_message = event.message.text

        applied_word_list = [word for word in reply_list if word in user_message]

        if len(applied_word_list) > 1:
            reply_message = "よくわかりません^_^"
        elif "昨日" in user_message:
            reply_message = get_weather_history(-1)
        elif "今日" in user_message:
            reply_message = get_weather(0)
        elif "明日" in user_message:
            reply_message = get_weather(1)
        else:
            reply_message = "話しかけないでください^_^"

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_message)
        )

    return ""


def get_weather_history(day_diff):
    YAKT = timezone(timedelta(hours=+9), "YAKT")
    dt_now = datetime.now(YAKT)
    dt = dt_now + timedelta(day_diff)
    dt_str = dt.strftime("%Y/%m/%d %H:%M")
    unix_dt = dt.timestamp()
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
    weather_info = weather_json["data"]
    japanese_weather_list = ["晴れ", "曇り", "雨", "雪"]
    english_weather_list = ["Clear", "Clouds", "Rain", "Snow"]
    weather = weather_info["weather"][0]["main"]
    if weather in english_weather_list:
        weather = japanese_weather_list[english_weather_list.index(weather)]
    temperature = weather_info["temp"]
    feel_like = weather_info["feels_like"]
    humidity = weather_info["humidity"]
    message = f"{dt_str} (YAKT) のヤクーツク\n天気: {weather} \n気温: {temperature}℃\n体感温度: {feel_like}℃\n湿度: {humidity}%"
    return message


def get_weather(day_diff):
    response = requests.get(
        "https://api.openweathermap.org/data/3.0/onecall",
        params={
            "lat": 62.0397,
            "lon": 129.7422,
            "exclude": "current,minutely,hourly,alerts",
            "appid": WEATHER_API_KEY,
            "units": "metric",
            "lang": "ja",
        },
    )
    weather_json = json.loads(response.text)
    weather_info = weather_json["daily"][day_diff]
    YAKT = timezone(timedelta(hours=+9), "YAKT")
    dt_now = datetime.now(YAKT)
    dt = dt_now + timedelta(day_diff)
    dt_str = dt.strftime("%Y/%m/%d %H:%M")
    japanese_weather_list = ["晴れ", "曇り", "雨", "雪"]
    english_weather_list = ["Clear", "Clouds", "Rain", "Snow"]
    weather = weather_info["weather"][0]["main"]
    if weather in english_weather_list:
        weather = japanese_weather_list[english_weather_list.index(weather)]
    temperature = weather_info["temp"]
    feel_like = weather_info["feels_like"]
    humidity = weather_info["humidity"]
    message = f"{dt_str} (YAKT) のヤクーツク\n天気: {weather} \n気温: {temperature}℃\n体感温度: {feel_like}℃\n湿度: {humidity}%"
    return message
