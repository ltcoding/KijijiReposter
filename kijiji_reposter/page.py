from element import ClickableElement, ConfirmationTextElement, FileUploadButtonElement
from element import TextFormElement, DropdownElement, ConfirmPresenceNElems
from locators import AdsPageLocator, PostAdPageLocator
from configkeys import ConfigKeys
import logging
import time

from urllib.parse import urlencode
#from urllib.parse import urlunparse
#from urllib.parse import urljoin
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

    def __init__(self, driver, ad_params=None):
        super().__init__(driver)
        self.ad_params = ad_params

        self.curbside_button = ClickableElement(PostAdPageLocator.CURBSIDE_BUTTON)
        self.cashless_button = ClickableElement(PostAdPageLocator.CASHLESS_BUTTON)
        self.desc_body = TextFormElement(PostAdPageLocator.DESC_TEXT_FORM)
        self.price_text = TextFormElement(PostAdPageLocator.PRICE_TEXT_FORM)

        self.size_dropdown = DropdownElement(PostAdPageLocator.SIZE_DROPDOWN)
        self.file_upload_button = FileUploadButtonElement(PostAdPageLocator.FILE_UPLOAD_BUTTON)
        self.img_upload_success = ConfirmPresenceNElems(PostAdPageLocator.IMG_UPLOAD_SUCCESS)

        self.submit_button = ClickableElement(PostAdPageLocator.SUBMIT_BUTTON)
        self.post_success_text = ConfirmationTextElement(PostAdPageLocator.POST_SUCCESS_TEXT)

    def open(self, ad_params=None):
        self.logger.info("Visting Post Ads page")

        if ad_params is None:
            url = PostAdPage.URL
        else:
            data = {'categoryId': ad_params[ConfigKeys.CATID], 'adTitle': ad_params[ConfigKeys.TITLE]}
            print(ad_params[ConfigKeys.CATID])
            #print(len(ad_params[ConfigKeys.CATID]), ad_params[ConfigKeys.CATID])

            parsed = urlparse(PostAdPage.URL)._replace(query=urlencode(data))
            url = parsed.geturl()
            #url = urljoin(PostAdPage.URL, urlencode(data))

        #if ad_params:
        #    url = PostAdPage.URL_FORMAT.format(
        #        categoryId=ad_params[ConfigKeys.CATID], 
        #        adTitle=ad_params[ConfigKeys.TITLE]
        #    )
        #else:
        #    url = PostAdPage.URL
        # url = PostAdPage.URL
        print(url)
        self.driver.get(url)


    def post_ad(self, ad_params):
        
        status = True 
        
        print(self.driver.title)
        if ad_params.get(ConfigKeys.CURBSIDE, False):
            status = self.curbside_button.click("Clicking curbside button", self.driver) and status
            self.driver.save_screenshot('curbside.png')
        if ad_params.get(ConfigKeys.CASHLESS, False):
            status = self.cashless_button.click("Clicking cashless button", self.driver) and status
            self.driver.save_screenshot('cashless.png')
        if ad_params.get(ConfigKeys.SIZE, False):
            status = self.size_dropdown.select_dropdown(
                "Selecting size in dropdown", self.driver, ad_params[ConfigKeys.SIZE]) and status
            self.driver.save_screenshot('dropdown.png')

        imgs = '\n'.join(ad_params[ConfigKeys.IMGS])
        self.desc_body.fill_text_form("Filling description text", self.driver, ad_params[ConfigKeys.DESC])
        self.driver.save_screenshot('desc_txt.png')
        self.price_text.fill_text_form("Filling price text", self.driver, ad_params[ConfigKeys.PRICE])
        self.driver.save_screenshot('price.png')
        print(ad_params[ConfigKeys.IMGS])
        self.file_upload_button.upload_files("Uploading pictures", self.driver, imgs)
        #time.sleep(10)
        nimg = len(ad_params[ConfigKeys.IMGS])
        self.img_upload_success.confirm("Confirming images uploaded", self.driver, nimg)
        #ele = self.driver.find_element("xpath", '//div[@class="react-grid-layout layout"]')
        #total_height = ele.size["height"] + 1000
        #self.driver.set_window_size(1920, total_height)
        #el = self.driver.find_element_by_tag_name('body')
        #el.screenshot('uploaded.png')
        #time.sleep(2)
        #self.driver.find_element("xpath", "//li/div[@class='image-area']")
        #self.driver.find_element("xpath", "//h3[text()='Add photos to attract interest to your ad']")
        
        #time.sleep(2)
        self.driver.save_screenshot('upload_files.png')
        self.submit_button.click("Clicking submit button", self.driver)
        #time.sleep(10)
        self.post_success_text.confirm("Confirming post success", self.driver)
        self.driver.save_screenshot('after_submit.png')

#        if status and \
#            self.desc_body.fill_text_form("Filling description text", self.driver, ad_params[ConfigKeys.DESC]) and \
#            self.price_text.fill_text_form("Filling price text", self.driver, ad_params[ConfigKeys.PRICE]) and \
#            self.file_upload_button.upload_files("Uploading pictures", self.driver, imgs) and \
#            self.submit_button.click("Clicking submit button", self.driver):
#
#            self.driver.save_screenshot('hello.png')
#            
#            return True 

        return False 
