from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from page import AdsPage
import logging
from datetime import datetime
import os


class KijijiReposter(object):

    COOKIE_NAME = 'ssid'
    HOMEPAGE = 'https://www.kijiji.ca'

    def __init__(self, cookie_filename='tk.txt', logger_name=__name__, log_filename='kijiji_reposter.log',
                 log_level=logging.INFO):
        self.opts = Options()
        self.opts.headless = True

#        self.driver = webdriver.Firefox(options=opts)
        self.driver = webdriver.Chrome(options=self.opts)

        self.cookie_filename = cookie_filename
        self.cookie = None

        self.log_filename = log_filename
        self.log_level = log_level
        self.logger_name = logger_name
        self._init_logger()
        
#        utils.log.init_logger(log_filename, log_level, 'base')
#        self.logger = utils.log.my_getLogger(logger_name)


    def _init_logger(self):
        
        basename, ext = os.path.splitext(self.log_filename)
        filename = '_'.join([basename, datetime.today().strftime('%Y%m%d_%H%M%S')])
        logging.basicConfig(
            filename=filename + ext, 
            level=self.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        )

        self.logger = logging.getLogger(self.logger_name)

#        self.handler = logging.FileHandler(self.log_filename)
#        self.handler.setLevel(self.log_level)
#        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#        self.handler.setFormatter(self.formatter)
#
#        self.logger = logging.getLogger(self.logger_name)        
#        self.logger.addHandler(self.handler)
#        self.logger.setLevel(self.log_level)

    def login(self):
        self.logger.info('Connecting to homepage')
        self.driver.get(KijijiReposter.HOMEPAGE)
        if self.cookie is None:
            self.logger.info('Reading cookie file')
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
