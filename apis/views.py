from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage
from account_manager.utils import register, get_user_info
from selenium_agent.web_crawler import WebCrawler

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
web_crawler = WebCrawler(driver='remote')


# Create your views here.
@csrf_exempt
def entry(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        # get request body as text
        body = request.body.decode('utf-8')

        # handle webhook body
        try:
            handler.handle(body, signature)
        except LineBotApiError as e:
            print(e)
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@handler.add(MessageEvent, message=TextMessage)
def message_text(event: MessageEvent):
    cmd = event.message.text.split('\n')[0]
    reply_msg = None
    match cmd:
        case "@帳號綁定":
            bind_account(event)
        case "@帳號設置":
            # 已經在line account manager設定自動回覆
            pass
        case "@點餐":
            order(event)
        case "@查看點餐紀錄與使用者資訊":
            error_code, user_info = check_order_and_user_info(event)
            if not error_code:
                reply_msg = f'帳號已綁定\n' + user_info
            else:
                reply_msg = f'帳號尚未綁定,請進行綁定'
        case "@聯絡管理員":
            reply_msg = f"哩賀 哇細Jason直接來座位找我吧"
        case _:
            reply_msg = f'訊息格式錯誤，請聯絡管理員'
    if reply_msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg)
        )


def bind_account(event: MessageEvent):
    try:
        formatted_msg = event.message.text.split('\n')
        employee_id = formatted_msg[1].split(":")[1]
        name = formatted_msg[2].split(":")[1]
        corporation = formatted_msg[3].split(":")[1]
        person, created = register(line_user_id=event.source.user_id, employee_id=employee_id, name=name,
                                   corporation=corporation)
        if created:
            reply_msg = f'帳號綁定成功'
        else:
            reply_msg = f'帳號設定已更新'
    except Exception as e:
        print(e)
        reply_msg = f'帳號綁定失敗,請聯絡管理員'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_msg)
    )


def check_order_and_user_info(event: MessageEvent):
    error_code = 0
    try:
        p = model_to_dict(get_user_info(event.source.user_id))
        user_info = (f'姓名:{p["name"]}\n'
                     f'工號:{p["employee_id"]}\n'
                     f'法人:{p["corporation"]}')
    except Exception as e:
        print(e)
        return 1, None
    return error_code, user_info


def order(event: MessageEvent):
    meals = web_crawler.get_menu()
    reply_msg = ''
    for meal in meals:
        reply_msg += f'{meal}\n'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_msg)
    )
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Jason')
    )
