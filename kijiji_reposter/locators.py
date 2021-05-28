from selenium.webdriver.common.by import By


class AdsPageLocator(object):
    """A class for My Ads Page locators"""

    DELETE_BUTTON = (By.XPATH, "//button[@data-qa-id='adDeleteButton']")
    DELETE_REASON_BUTTON = (By.XPATH, "//button[text() = 'Prefer not to say']")
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[text() = 'Delete listing']")
    XWINDOW_DELETE_BUTTON = (By.ID, 'modalCloseButton')
    DELETE_SUCCESS_TEXT = (By.XPATH, "//span[text() = 'deleted']")
    

class PostAdPageLocator(object):

     CASHLESS_BUTTON = (By.XPATH, "//label[@for='payment_s-cashless']")
     CURBSIDE_BUTTON = (By.XPATH, '//label[@for="fulfillment_s-curbside"]')
     DESC_TEXT_FORM = (By.ID, "pstad-descrptn")
     PRICE_TEXT_FORM = (By.ID, "PriceAmount")     
     SIZE_DROPDOWN = (By.ID, "size_s")
     #FILE_UPLOAD_BUTTON = (By.ID, "html5_1f6ob4ave1ht5clhmr1i2614tk3")
     FILE_UPLOAD_BUTTON = (By.XPATH, '//div[@class="imageUploadButtonWrapper"]//input[@type="file"]')
     #FILE_UPLOAD_BUTTON = (By.XPATH, "//li/div[@class='image-area']")
     SUBMIT_BUTTON = (By.XPATH, "//button[@name='saveAndCheckout']")
     POST_SUCCESS_TEXT = (By.XPATH, "//h3[contains(text(),'success')]")
     # IMG_UPLOAD_SUCCESS = (By.XPATH, '//div[@class="image" and contains(@style,"ebayimg")]')
     # IMG_UPLOAD_SUCCESS = (By.XPATH, '//li[@class="thumbnail"]//div[@class="image" and contains(@style,"ebayimg")]')
     IMG_UPLOAD_SUCCESS = (By.XPATH, 
        '//ol[@id="MediaUploadedImages"]//div[@class="spinner animate-spin-kj-icon-spin4"]')
     #IMG_UPLOAD_SUCCESS = (By.XPATH, 
     #   '//ol[@id="MediaUploadedImages"]/li[@class="thumbnail" or @class="thumbnail selected"]')
