from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

class KijijiReposter(object):

    COOKIE_NAME = 'ssid'

    def __init__(self, cookie_filename='tk.txt'):
        opts = Options()
        opts.headless = True
#        self.driver = webdriver.Firefox(options=opts)
        self.driver = webdriver.Chrome(options=opts)
        self.cookie_filename = cookie_filename
        self.cookie = None

    def login(self):
        self.driver.get('https://www.kijiji.ca')
        if self.cookie is None:
            with open(self.cookie_filename, 'r') as f:
                self.cookie = f.read().strip()
        self.driver.add_cookie({'name': KijijiReposter.COOKIE_NAME, 'value': self.cookie})

    def delete_all_ads(self):
        self.driver.get('https://www.kijiji.ca/m-my-ads/active/1')
        button_ls = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[@data-qa-id='adDeleteButton']"))
        )
#        print(button_ls)
        print(len(button_ls))
        for button in button_ls[:1]:
            button.click()
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[text() = 'Prefer not to say']"))
            )
            print(button)
            button.click()

            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[text() = 'Delete listing']"))
            )
            print(button)
            button.click()

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
