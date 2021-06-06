from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from page import AdsPage, PostAdPage
import adstats

import logging
import datetime
import os
import sys
import argparse

import yaml
import csv

from configkeys import ConfigKeys


class KijijiReposter(object):

    COOKIE_NAME = 'ssid'
    HOMEPAGE = 'https://www.kijiji.ca'
    AD_IDS_FILENAME = 'ad_ids.yaml'
    STATS_FILENAME = 'stats.csv'
    TITLE2DIR_FILENAME = 'title2dir.json'
    DATE_FORMAT = '%Y-%m-%d'
    MAX_LEN_TITLE = 64
    DRIVER_PAGE_TIMEOUT = 60

    def __init__(self, cookie_filename='tk.txt', logger_name=__name__, log_filename='kijiji_reposter.log',
                 log_level=logging.INFO, ad_ids_filename=AD_IDS_FILENAME, is_track=False):

        self.opts = Options()
        self.opts.add_argument('--start-maximized')

        self.driver = webdriver.Chrome(options=self.opts)
        self.driver.set_page_load_timeout(KijijiReposter.DRIVER_PAGE_TIMEOUT)

        self.cookie_filename = cookie_filename
        self.cookie = None

        self.log_filename = log_filename
        self.log_level = log_level
        self.logger_name = logger_name
        self._init_logger()

        self.ad_ids_filename = ad_ids_filename
        self.load_ad_ids()
        
        self.title2dir = {}

        self.is_track = is_track


    def _init_logger(self):
        
        basename, ext = os.path.splitext(self.log_filename)
        filename = '_'.join([basename, datetime.datetime.today().strftime('%Y%m%d_%H%M%S')])

        file_handler = logging.FileHandler(filename=filename + ext)
        stdout_handler = logging.StreamHandler(sys.stdout)

        logging.basicConfig(
            level=self.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
            handlers=[file_handler, stdout_handler]
        )

        self.logger = logging.getLogger(self.logger_name)

    def load_ad_ids(self):

        if os.path.isfile(self.ad_ids_filename):
            with open(self.ad_ids_filename, 'r') as f:
                self.ad_ids = yaml.safe_load(f)
            if not isinstance(self.ad_ids, dict):
                self.logger.warn(f'adIds file {self.ad_ids_filename} does not contain dict')
                self.ad_ids = {}
        else:
            self.ad_ids = {}
        
    @staticmethod
    def load_ad_config(filename):
        with open(filename, 'r') as f:
            ad_config = yaml.safe_load(f)
        
        if len(ad_config[ConfigKeys.TITLE]) > KijijiReposter.MAX_LEN_TITLE:
            self.logger.warn("Title being truncated to max length")
            ad_config[ConfigKeys.TITLE] = \
                ad_config[ConfigKeys.TITLE][:KijijiReposter.MAX_LEN_TITLE]

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

    def walk(self, rootdir):
        
        for basedir, subdirs, files in os.walk(rootdir):
            if ConfigKeys.CONFIG_FILE not in files:
                continue
            config_file = os.path.join(basedir, ConfigKeys.CONFIG_FILE)
            ad_config = self.load_ad_config(config_file)

            yield (basedir, subdirs, files, ad_config)

    def load_title2dir(self, rootdir):
        
        for basedir, subdirs, files, ad_config in self.walk(rootdir):
            title = ad_config.get(ConfigKeys.TITLE, '').strip()
            self.title2dir[title] = basedir

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
        return post_ads_page.post(ad_config)

    def post_all_ads(self, rootdir):
        
        cnt = 1

        for basedir, subdirs, files, ad_config in self.walk(rootdir):

            self.logger.info(f"Posting ad number {cnt}: {ad_config[ConfigKeys.TITLE]}")
            posted_ad_id = self.post_ad(ad_config)
            
            if posted_ad_id:
                self.ad_ids[basedir] = posted_ad_id[ConfigKeys.AD_ID]
            cnt += 1

        with open(self.ad_ids_filename, 'w') as f:
           yaml.safe_dump(self.ad_ids, f, default_style=None, default_flow_style=False) 

    @staticmethod
    def _add_year2date(kijiji_date, year):
        s = str(year) + ' ' + kijiji_date
        return datetime.datetime.strptime(s, AdsPage.DATE_FORMAT)

    @staticmethod
    def kijijidate2datetime(kijiji_date):
        """Convert kijiji formatted date (month and day) to datetime"""

        today = datetime.datetime.today()
        year = today.year

        candidate_date = KijijiReposter._add_year2date(kijiji_date, year)
        candidate_date = candidate_date if candidate_date <= today else \
            KijijiReposter._add_year2date(kijiji_date, year - 1)

        return candidate_date.strftime(KijijiReposter.DATE_FORMAT)

    def _process_stats(self, stats):

        config_file = os.path.join(self.title2dir[stats[adstats.TITLE]], 
            ConfigKeys.CONFIG_FILE)
        imgs = self.load_ad_config(config_file)[ConfigKeys.IMGS]
        
        stats[adstats.MAIN_IMG] = os.path.basename(imgs[0]) if imgs else ''
        stats[adstats.DATE_DELETED] = datetime.datetime.today().strftime(
            KijijiReposter.DATE_FORMAT)
        stats[adstats.DATE_POSTED] = KijijiReposter.kijijidate2datetime(
            stats[adstats.DATE_POSTED])

    def write_stats(self, stats):
        
        self._process_stats(stats)
            
        filename = os.path.join(
            self.title2dir[stats[adstats.TITLE]], KijijiReposter.STATS_FILENAME
        )
        is_file_exists = os.path.isfile(filename)
        with open(filename, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=adstats.schema)
            if not is_file_exists:
                writer.writeheader()
            writer.writerow(stats)

    def delete_all_ads(self, rootdir):

        ads_page = AdsPage(self.driver)
        ads_page.open()

        self.load_title2dir(rootdir)
        
        i = 0
        while True:
            i += 1
            self.logger.info(f"Deleting ad {i}")

            stats = ads_page.delete_first_ad()
            if not stats:
                break

            if self.is_track:
                self.write_stats(stats)
                

    def cleanup(self):
        self.driver.delete_cookie(KijijiReposter.COOKIE_NAME)
        self.driver.close()

    def repost(self, rootdir, delete_all=False, is_post=False):
        self.login()
        if delete_all:
            self.delete_all_ads(rootdir)
        if is_post:
            self.post_all_ads(rootdir)
        self.cleanup()


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description="""Deletes all ads currently listed and reposts"""
    )
    
    parser.add_argument('-c', '--cookie_file', 
                        help="""Filename of text file containing SSID cookie used for signing in""", 
                        required=True,
                        default='',
                        type=str)

    parser.add_argument('-r', '--rootdir', 
                        help="""Root directory containing ad config files in subdirectories""", 
                        required=False,
                        default='',
                        type=str)

    parser.add_argument('-d', '--delete_all', 
                        help="""Flag to delete all currently posted ads""", 
                        required=False,
                        action='store_true')

    parser.add_argument('-p', '--post', 
                        help="""Flag to post ads""", 
                        required=False,
                        action='store_true')

    parser.add_argument('-t', '--track_stats', 
                        help="""Flag for whether to track views/replies when ads are deleted""", 
                        required=False,
                        action='store_true')

    parser.add_argument('-l', '--log_filename', 
                        help="""File to log all events to""", 
                        required=False,
                        default='kijiji_reposter.log',
                        type=str)

    arg = parser.parse_args()

    kr = KijijiReposter(
        cookie_filename=arg.cookie_file,
        is_track=arg.track_stats,
        log_filename=arg.log_filename
    )

    kr.repost(
        rootdir=arg.rootdir,
        delete_all=arg.delete_all,
        is_post=arg.post
    )

