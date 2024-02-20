from celery import shared_task
from linebot import LineBotApi
from django.conf import settings
from linebot.models import TextSendMessage
from selenium_agent.web_crawler import WebCrawler, get_ordered_list
from account_manager.models import Person

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
web_crawler = WebCrawler(driver='remote')


@shared_task
def send_daily_menu():
    meals = web_crawler.get_menu()
    reply_msg = '今日餐點如下\n\n'
    for meal in meals:
        reply_msg += f'{meal}\n'
    reply_msg += '\n請記得點餐!'
    line_bot_api.broadcast(TextSendMessage(text=reply_msg))


@shared_task
def send_order_notify():
    ordered_list = get_ordered_list()
    for person in Person.objects.all():
        if person.name not in ordered_list:
            line_bot_api.push_message(
                person.line_user_id,
                TextSendMessage(
                    text='系統偵測尚未點餐，請記得點餐！'
                ))
