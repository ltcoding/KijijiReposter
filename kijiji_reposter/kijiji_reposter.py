from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from page import AdsPage


class KijijiReposter(object):

    COOKIE_NAME = 'ssid'

    def __init__(self, cookie_filename='tk.txt'):
        self.opts = Options()
        self.opts.headless = True

#        self.driver = webdriver.Firefox(options=opts)
        self.driver = webdriver.Chrome(options=self.opts)

        self.cookie_filename = cookie_filename
        self.cookie = None

    def login(self):
        self.driver.get('https://www.kijiji.ca')
        if self.cookie is None:
            with open(self.cookie_filename, 'r') as f:
                self.cookie = f.read().strip()
        self.driver.add_cookie({'name': KijijiReposter.COOKIE_NAME, 'value': self.cookie})

    def delete_all_ads(self):
        ads_page = AdsPage(self.driver)
        ads_page.open()
        ads_page.delete_first_ad()

    def cleanup(self):
        self.driver.delete_cookie(KijijiReposter.COOKIE_NAME)
        self.driver.close()

    def repost(self):
        self.login()
        self.delete_all_ads()
        self.cleanup()


if __name__ == '__main__':
    kr = KijijiReposter()
    kr.repost()
