from selenium.webdriver.common.by import By


class AdsPageLocator(object):
    """A class for My Ads Page locators"""

    VIEWS = 0
    REPLIES = 1
    PAGE_NO = 2

    DELETE_BUTTON = (By.XPATH, "//button[@data-qa-id='adDeleteButton']")
    DELETE_REASON_BUTTON = (By.XPATH, "//button[text() = 'Prefer not to say']")
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[text() = 'Delete listing']")
    XWINDOW_DELETE_BUTTON = (By.ID, 'modalCloseButton')
    DELETE_SUCCESS_TEXT = (By.XPATH, "//span[text() = 'deleted']")
    TITLE = (By.XPATH, '//h2[@class="title-3111867204"]/a')
    STATS_CONTAINER = (By.XPATH, '//div[@class="stats-2792068901"]')
    INNER_STATS = (By.TAG_NAME, 'span')
    POSTED_DATE = (By.XPATH, '//time[@class="posted-801946228"]/span')
    PRICE = (By.XPATH, '//div[@class="price-3759726252"]/span[@class="value-3804164946"]/span')
    

class PostAdPageLocator(object):

     CASHLESS_BUTTON = (By.XPATH, "//label[@for='payment_s-cashless']")
     CURBSIDE_BUTTON = (By.XPATH, '//label[@for="fulfillment_s-curbside"]')
     DESC_TEXT_FORM = (By.ID, "pstad-descrptn")
     PRICE_TEXT_FORM = (By.ID, "PriceAmount")     
     SIZE_DROPDOWN = (By.ID, "size_s")
     FILE_UPLOAD_BUTTON = (By.XPATH, '//div[@class="imageUploadButtonWrapper"]//input[@type="file"]')
     SUBMIT_BUTTON = (By.XPATH, "//button[@name='saveAndCheckout']")
     POST_SUCCESS_TEXT = (By.XPATH, "//h3[contains(text(),'success')]")
     IMG_UPLOAD_SUCCESS = (By.XPATH, '//ol[@id="MediaUploadedImages"]//div[@class="spinner animate-spin kj-icon-spin4"]')
     AD_ID = (By.XPATH, '//a[@class="adId-4111206830"]')
    
