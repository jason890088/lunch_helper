from celery import shared_task
from linebot import LineBotApi
from django.conf import settings
from linebot.models import TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


@shared_task
def send_daily_notify():
    line_bot_api.broadcast(TextSendMessage(text='hello world'))