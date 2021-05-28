from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from page import AdsPage, PostAdPage
import logging
from datetime import datetime
import os
import sys
import argparse

import yaml

from configkeys import ConfigKeys


class KijijiReposter(object):

    COOKIE_NAME = 'ssid'
    HOMEPAGE = 'https://www.kijiji.ca'

    def __init__(self, cookie_filename='tk.txt', logger_name=__name__, log_filename='kijiji_reposter.log',
                 log_level=logging.INFO):
        self.opts = Options()
        # self.opts.add_argument('--start-fullscreen')
        self.opts.add_argument('--start-maximized')
        # self.opts.headless = True

#        self.driver = webdriver.Firefox(options=opts)
        self.driver = webdriver.Chrome(options=self.opts)

        self.cookie_filename = cookie_filename
        self.cookie = None

        self.log_filename = log_filename
        self.log_level = log_level
        self.logger_name = logger_name
        self._init_logger()
        

    def _init_logger(self):
        
        basename, ext = os.path.splitext(self.log_filename)
        filename = '_'.join([basename, datetime.today().strftime('%Y%m%d_%H%M%S')])

        file_handler = logging.FileHandler(filename=filename + ext)
        stdout_handler = logging.StreamHandler(sys.stdout)

        logging.basicConfig(
            level=self.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
            handlers=[file_handler, stdout_handler]
        )

        self.logger = logging.getLogger(self.logger_name)

    @staticmethod
    def load_ad_config(filename):
        with open(filename, 'r') as f:
            ad_config = yaml.safe_load(f)
        
        if ConfigKeys.IMGS not in ad_config:
            return ad_config
        if len(ad_config[ConfigKeys.IMGS]) == 0:
            return ad_config

        # Append full path to image filename if not already present
        dirname = os.path.dirname(filename)

        ad_config[ConfigKeys.IMGS] = [
            x if os.path.dirname(x) else os.path.join(dirname, x) \
                for x in ad_config[ConfigKeys.IMGS]
        ]
        res = {key: val if not isinstance(val, str) else val.strip("\"\'")\
            for key, val in ad_config.items()}
        return res


    def login(self):
        self.logger.info('Connecting to homepage')
        self.driver.get(KijijiReposter.HOMEPAGE)
        if self.cookie is None:
            self.logger.info('Reading cookie file')
            with open(self.cookie_filename, 'r') as f:
                self.cookie = f.read().strip()
        self.driver.add_cookie({'name': KijijiReposter.COOKIE_NAME, 'value': self.cookie})

    def post_ad(self, ad_config):
        post_ads_page = PostAdPage(self.driver)
        post_ads_page.open(ad_config)
        post_ads_page.post_ad(ad_config)

    def post_all_ads(self, rootdir):
        
        cnt = 1
        for basedir, subdirs, files in os.walk(rootdir):
            print(basedir, subdirs, files)
            if ConfigKeys.CONFIG_FILE not in files:
                continue

            self.logger.info(f"Posting ad number {cnt}")
            config_file = os.path.join(basedir, ConfigKeys.CONFIG_FILE)
            ad_config = self.load_ad_config(config_file)
            print(ad_config)
            self.post_ad(ad_config)
            cnt += 1

    def ls_config_files(self, rootdir):
        config_files = [
            os.path.join(root, filename) for (root, dirs, files) in os.walk(rootdir) \
               for filename in files if filename == 'ad_config.yaml'
        ]
        return config_files

    def delete_all_ads(self):
        ads_page = AdsPage(self.driver)
        ads_page.open()
        ads_page.delete_first_ad()

    def cleanup(self):
        self.driver.delete_cookie(KijijiReposter.COOKIE_NAME)
        self.driver.close()

    def repost(self, rootdir):
        self.login()
        # self.delete_all_ads()
        self.post_all_ads(rootdir)
        self.cleanup()


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description="""Deletes all ads currently listed and reposts"""
    )
    
    parser.add_argument('-r', '--rootdir', 
                        help="""Root directory containing ad config files in subdirectories""", 
                        required=False,
                        default='',
                        type=str)

    arg = parser.parse_args()

    kr = KijijiReposter()
    kr.repost(rootdir=arg.rootdir)

