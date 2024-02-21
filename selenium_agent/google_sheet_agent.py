import pygsheets
from dotenv import load_dotenv


def get_ordered_list():
    # 讀取 .env 內的GOOGLE_SERVICE_ACCOUNT_CERT
    # 可參考 https://hackmd.io/@Yun-Cheng/GoogleSheets
    google_client = pygsheets.authorize(service_account_env_var='GOOGLE_SERVICE_ACCOUNT_CERT')
    url = 'https://docs.google.com/spreadsheets/d/109aWZaPfGXen7xhGnC6ISC-7Sauj8GemuTZ8infwdlw/edit#gid=898178581'
    sheet = google_client.open_by_url(url)
    worksheet = sheet.worksheet_by_title("表單回應 1").get_as_df()
    return worksheet['您的名字'].to_list()


def main():
    load_dotenv()  # loads the configs from .env
    print(get_ordered_list())


if __name__ == '__main__':
    main()
