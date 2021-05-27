from element import ClickableElement, ConfirmationTextElement
from locators import AdsPageLocator
import logging


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
        self.delete_successful_text = ConfirmationTextElement(AdsPageLocator.DELETE_SUCCESS_TEXT)
        self.close_delete_window_button = ClickableElement(AdsPageLocator.XWINDOW_DELETE_BUTTON)


    def open(self):
        self.logger.info('Visiting Ads Page')
        self.driver.get(AdsPage.ADS_URL)


    def delete_first_ad(self):
        if self.delete_button.click("Clicking delete", self.driver) and \
            self.delete_reason_button.click('Clicking delete reason', self.driver) and \
            self.delete_confirm_button.click('Clicking confirm delete', self.driver) and \
            self.delete_successful_text.confirm('Finding delete confirmation', self.driver) and \
            self.close_delete_window_button.click('Closing delete window', self.driver):
#        if self.log_action('Clicking delete', self.delete_button.click, self.driver) and \
#            self.log_action('Clicking delete reason', self.delete_reason_button.click, self.driver) and \
#            self.log_action('Clicking confirm delete', self.delete_confirm_button.click, self.driver) and \
#            self.log_action('Finding delete confirmation', self.delete_successful_text.confirm, self.driver) and \
#            self.log_action('Closing delete window', self.close_delete_window_button.click, self.driver):

            return True 
        
        return False
