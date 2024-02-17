from celery import shared_task
from linebot import LineBotApi
from django.conf import settings
from linebot.models import TextSendMessage
from selenium_agent.web_crawler import WebCrawler

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
web_crawler = WebCrawler(driver='remote')


@shared_task
def send_daily_notify():
    meals = web_crawler.get_menu()
    reply_msg = '今日餐點如下\n\n'
    for meal in meals:
        reply_msg += f'{meal}\n'
    reply_msg += '\n請記得點餐!'
    line_bot_api.broadcast(TextSendMessage(text=reply_msg))
