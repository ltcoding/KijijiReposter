from element import ClickableElement, ConfirmationTextElement
from locators import AdsPageLocator


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver


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
        self.driver.get(AdsPage.ADS_URL)


    def delete_first_ad(self):
#        is_delete_click = self.delete_button.click(self.driver) #self.delete_button.__get__(self, AdsPage)
#        if not is_delete_click:
#            print("not found")
#            return False
#        is_delete_reason_click = self.delete_reason_button.__get__(self, AdsPage)
#        is_delete_confirm_click = self.delete_confirm_button.__get__(self, AdsPage)
#        is_delete_successful = self.delete_successful_text.__get__(self, AdsPage)
#        is_delete_xwindow_click = self.close_delete_window_button.__get__(self, AdsPage)
#        print(is_delete_click, is_delete_reason_click, is_delete_confirm_click, is_delete_successful, is_delete_xwindow_click)
#        print(is_deleted)
        if self.delete_button.click(self.driver) and \
            self.delete_reason_button.click(self.driver) and \
            self.delete_confirm_button.click(self.driver) and \
            self.delete_successful_text.confirm(self.driver) and \
            self.close_delete_window_button.click(self.driver):

            print("Successful delete")
            return True 
        
        print("Unsuccessful delete")
        return False
