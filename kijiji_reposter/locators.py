from selenium.webdriver.common.by import By


class AdsPageLocator(object):
    """A class for My Ads Page locators"""

    DELETE_BUTTON = (By.XPATH, "//button[@data-qa-id='adDeleteButton']")
    DELETE_REASON_BUTTON = (By.XPATH, "//button[text() = 'Prefer not to say']")
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[text() = 'Delete listing']")
    XWINDOW_DELETE_BUTTON = (By.ID, 'modalCloseButton')
    DELETE_SUCCESS_TEXT = (By.XPATH, "//span[text() = 'deleted']")
    
