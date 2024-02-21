import pygsheets
from dotenv import load_dotenv
from datetime import date, timedelta, datetime


def get_ordered_list():
    # 讀取 .env 內的GOOGLE_SERVICE_ACCOUNT_CERT
    # 可參考 https://hackmd.io/@Yun-Cheng/GoogleSheets
    google_client = pygsheets.authorize(service_account_env_var='GOOGLE_SERVICE_ACCOUNT_CERT')
    url = 'https://docs.google.com/spreadsheets/d/109aWZaPfGXen7xhGnC6ISC-7Sauj8GemuTZ8infwdlw/edit#gid=898178581'
    sheet = google_client.open_by_url(url)
    worksheet = sheet.worksheet_by_title("表單回應 1").get_as_df()
    user_list = []
    # google sheet有折疊,需要另外過濾已折疊資料
    for idx, row in worksheet.iterrows():
        user_datetime = row['時間戳記']
        if time_filter(user_datetime):
            user_list.append(row['您的名字'])
    return user_list


def time_filter(user_datetime):
    user_date = datetime.strptime(user_datetime.split(' ')[0], "%Y/%m/%d").date()
    time_range = user_datetime.split(' ')[1]
    today = date.today()
    if user_date == (today - timedelta(days=1)) and time_range == '下午':
        return True
    elif user_date == today and time_range == '上午':
        return True
    else:
        return False


def main():
    load_dotenv()  # loads the configs from .env
    print(get_ordered_list())


if __name__ == '__main__':
    main()
