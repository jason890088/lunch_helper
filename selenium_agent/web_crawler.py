from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import datetime


class WebCrawler:
    def __init__(self, driver=None):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("-incognito")
        self.order_url = 'https://docs.google.com/forms/d/e/1FAIpQLSe5jxs_7rCkhvqSDzUdInJs_cYsiEmzlOzFw7Q4p8KwJncP4A/viewform?pli=1&fbzx=-715767029344563818'
        self.command_executor = 'http://selenium-hub:4444/wd/hub'
        self.driver = driver

    def create_order_form(self, name='點餐仔', employee_id=8888, corp='鴻海'):
        if self.driver:
            driver = webdriver.Remote(
                command_executor=self.command_executor,
                options=self.option
            )
        else:
            driver = webdriver.Chrome(options=self.option)
        driver.get(self.order_url)
        time.sleep(3)

        # 填寫姓名
        name_input = driver.find_element(
            By.XPATH,
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
        )
        name_input.send_keys(name)

        # 填寫工號
        employee_id_input = driver.find_element(
            By.XPATH,
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
        )
        employee_id_input.send_keys(str(employee_id))

        # 填寫法人
        driver.execute_script("window.scrollTo(0, 1080)")
        corp_button = driver.find_element(
            By.XPATH,
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]',
        )
        corp_button.click()
        time.sleep(1)
        corp_selector = driver.find_element(
            By.XPATH,
            f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[2]//span[@class="vRMGwf oJeWuf" and text()="{corp}"]'
        )
        corp_selector.click()
        time.sleep(1)

        return driver

    def get_menu(self):
        supplier_list = ['東發排骨便當', '樂坡蔬食健康餐']
        meals = []
        for supplier in supplier_list:
            driver = self.create_order_form()
            # 填寫廠商
            supplier_button = driver.find_element(
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div[1]/div[1]'
            )
            supplier_button.click()
            time.sleep(1)
            supplier_selector = driver.find_element(
                By.XPATH,
                f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[2]//span[@class="vRMGwf oJeWuf" and text()="{supplier}"]'
            )
            supplier_selector.click()
            time.sleep(1)

            # 按下繼續
            continue_button = driver.find_element(
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span'
            )
            continue_button.click()
            time.sleep(1)

            # 獲得當日餐點
            items = driver.find_elements(
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div//span[@class="aDTYNe snByac OvPDhc OIC90c"]'
            )
            time.sleep(10)
            for item in items:
                meals.append(f'{supplier}-{item.text}')
            driver.quit()

        return meals


def main():
    web_crawler = WebCrawler()
    meals = web_crawler.get_menu()
    print(meals)


if __name__ == '__main__':
    main()
