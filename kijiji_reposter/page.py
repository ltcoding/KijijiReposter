from element import ClickableElement, ConfirmationTextElement, FileUploadButtonElement
from element import TextFormElement, DropdownElement, AppearDisappearElement 
from locators import AdsPageLocator, PostAdPageLocator
from configkeys import ConfigKeys
import logging
import time

from urllib.parse import urlencode
from urllib.parse import urlparse


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver, logger_name=__name__):
        self.driver = driver
        self.logger = logging.getLogger(logger_name)


class AdsPage(BasePage):
    """Page to view current ads"""

    ADS_URL = 'https://www.kijiji.ca/m-my-ads/active/1'

    def __init__(self, driver):
        super().__init__(driver)
        self.delete_button = ClickableElement(AdsPageLocator.DELETE_BUTTON)
        self.delete_reason_button = ClickableElement(AdsPageLocator.DELETE_REASON_BUTTON)
        self.delete_confirm_button = ClickableElement(AdsPageLocator.DELETE_CONFIRM_BUTTON)
        self.delete_success_text = ConfirmationTextElement(AdsPageLocator.DELETE_SUCCESS_TEXT)
        self.close_delete_window_button = ClickableElement(AdsPageLocator.XWINDOW_DELETE_BUTTON)


    def open(self):
        self.logger.info('Visiting Ads page')
        self.driver.get(AdsPage.ADS_URL)


    def delete_first_ad(self):
        if self.delete_button.click("Clicking delete", self.driver) and \
            self.delete_reason_button.click('Clicking delete reason', self.driver) and \
            self.delete_confirm_button.click('Clicking confirm delete', self.driver) and \
            self.delete_success_text.confirm('Finding delete confirmation', self.driver) and \
            self.close_delete_window_button.click('Closing delete window', self.driver):

            return True 
        
        return False


class PostAdPage(BasePage):

    URL = 'https://www.kijiji.ca/p-admarkt-post-ad.html'
    TIME_PER_UPLOAD = 5 

    def __init__(self, driver, ad_params=None):
        super().__init__(driver)
        self.ad_params = ad_params

        self.curbside_button = ClickableElement(PostAdPageLocator.CURBSIDE_BUTTON)
        self.cashless_button = ClickableElement(PostAdPageLocator.CASHLESS_BUTTON)
        self.desc_body = TextFormElement(PostAdPageLocator.DESC_TEXT_FORM)
        self.price_text = TextFormElement(PostAdPageLocator.PRICE_TEXT_FORM)

        self.size_dropdown = DropdownElement(PostAdPageLocator.SIZE_DROPDOWN)
        self.file_upload_button = FileUploadButtonElement(PostAdPageLocator.FILE_UPLOAD_BUTTON)
        self.img_upload_success = AppearDisappearElement(PostAdPageLocator.IMG_UPLOAD_SUCCESS)

        self.submit_button = ClickableElement(PostAdPageLocator.SUBMIT_BUTTON)
        self.post_success_text = ConfirmationTextElement(PostAdPageLocator.POST_SUCCESS_TEXT)
        self.ad_id_text = ConfirmationTextElement(PostAdPageLocator.AD_ID)

    def open(self, ad_params=None):
        self.logger.info("Visting Post Ads page")

        if ad_params is None:
            url = PostAdPage.URL
        else:
            data = {'categoryId': ad_params[ConfigKeys.CATID], 'adTitle': ad_params[ConfigKeys.TITLE]}

            parsed = urlparse(PostAdPage.URL)._replace(query=urlencode(data))
            url = parsed.geturl()

        self.driver.get(url)


    def post(self, ad_params):
        
        status = True 
        
        if ad_params.get(ConfigKeys.CURBSIDE, False):
            status = self.curbside_button.click("Clicking curbside button", self.driver) and status
        if ad_params.get(ConfigKeys.CASHLESS, False):
            status = self.cashless_button.click("Clicking cashless button", self.driver) and status
        if ad_params.get(ConfigKeys.SIZE, False):
            status = self.size_dropdown.select_dropdown(
                "Selecting size in dropdown", self.driver, ad_params[ConfigKeys.SIZE]) and status

        imgs = '\n'.join(ad_params[ConfigKeys.IMGS])
        nimg = len(ad_params[ConfigKeys.IMGS])

        if status and \
            self.desc_body.fill_text_form("Filling description text", self.driver, ad_params[ConfigKeys.DESC]) and \
            self.price_text.fill_text_form("Filling price text", self.driver, ad_params[ConfigKeys.PRICE]) and \
            self.file_upload_button.upload_files("Uploading pictures", self.driver, imgs) and \
            self.img_upload_success.confirm("Confirming images uploaded", self.driver, nimg * self.TIME_PER_UPLOAD) and \
            self.submit_button.click("Clicking submit button", self.driver) and \
            self.post_success_text.confirm("Confirming post success", self.driver):

            ad_id = self.ad_id_text.confirm('Finding Ad Id', self.driver).text
            return {ConfigKeys.AD_ID: ad_id}

        return None
