from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
import logging
import time


def log_action(func):

    def wrapper(self, msg, *args, **kwargs):
        has_logger = hasattr(self, "logger")
        if has_logger:
            self.logger.info(msg)

        status = func(self, *args, **kwargs)               
        if not status and has_logger:
            self.logger.warning("Failed")
        return status

    return wrapper


class BasePageElement(object):
    """Base page class that is initialized on every page object class."""

    TIMEOUT = 10

    def __init__(self, logger_name=__name__):
        self.logger = logging.getLogger(logger_name)

    def __set__(self, obj, value):
        """Sets the text to the value specified"""

        driver = obj.driver
        WebDriverWait(driver, BasePageElement.TIMEOUT).until(
            lambda driver: driver.find_element_by_name(self.locator))
        driver.find_element_by_name(self.locator).clear()
        driver.find_element_by_name(self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""

        driver = obj.driver
        WebDriverWait(driver, BasePageElement.TIMEOUT).until(
            lambda driver: driver.find_element_by_name(self.locator))
        element = driver.find_element_by_name(self.locator)
        return element.get_attribute("value")
        


class ClickableElement(BasePageElement):

    def __init__(self, locator):
        super().__init__()
        self.locator = locator

    @log_action
    def click(self, driver):
        try:
            clickable_item = WebDriverWait(driver, ClickableElement.TIMEOUT).until(
                EC.element_to_be_clickable(self.locator)
            )
            clickable_item.click()
        except TimeoutException as ex:
            return None 

        return clickable_item 


class NTextElements(BasePageElement):

    def __init__(self, locator):
        super().__init__()
        self.locator = locator

    @log_action
    def get(self, driver):
        try:
            elems = WebDriverWait(driver, BasePageElement.TIMEOUT).until(
                EC.presence_of_all_elements_located(self.locator)
            )
        except TimeoutException as ex:
            return None

        return elems


class ConfirmationTextElement(BasePageElement):

    def __init__(self, locator):
        super().__init__()
        self.locator = locator

    @log_action
    def confirm(self, driver):
        try:
            elem = WebDriverWait(driver, ConfirmationTextElement.TIMEOUT).until(
                EC.presence_of_element_located(self.locator)
            )
        except TimeoutException as ex:
            return None 

        return elem 


class TextFormElement(BasePageElement):

    def __init__(self, locator):
        super().__init__()
        self.locator = locator

    @log_action
    def fill_text_form(self, driver, text):
        try:
            text_form = WebDriverWait(driver, BasePageElement.TIMEOUT).until(
                EC.presence_of_element_located(self.locator)
            )
            text_form.clear()
            text_form.send_keys(text)
        except TimeoutException as ex:
            return None 

        return text_form

class DropdownElement(BasePageElement):

    def __init__(self, locator):
        super().__init__()
        self.locator = locator

    @log_action
    def select_dropdown(self, driver, value):

        try:
            dropdown = WebDriverWait(driver, BasePageElement.TIMEOUT).until(
                EC.presence_of_element_located(self.locator)
            )
            dropdown_select = Select(dropdown)
            dropdown_select.select_by_visible_text(value)
        except TimeoutException as ex:
            return None

        return dropdown


class FileUploadButtonElement(BasePageElement):

    def __init__(self, locator):
        super().__init__()
        self.locator = locator

    @log_action
    def upload_files(self, driver, value):
    
        try:
            input_element = WebDriverWait(driver, BasePageElement.TIMEOUT).until(
                EC.presence_of_element_located(self.locator)
            )
            input_element.send_keys(value)
        except TimeoutException as ex:
            return None

        return input_element


class AppearDisappearElement(BasePageElement):
    
    APPEAR_TIME = 4

    def __init__(self, locator):
        super().__init__()
        self.locator = locator

    @log_action
    def confirm(self, driver, timeout=BasePageElement.TIMEOUT):
        """
        Confirms that an element appears then becomes invisible. 
        Useful for progress bars etc
        """

        timeout_ = max(timeout, BasePageElement.TIMEOUT)

        try:
            #elems = WebDriverWait(driver, timeout_).until(
            #    EC.presence_of_element_located(self.locator)
            #)
            time.sleep(self.APPEAR_TIME)
            elems = WebDriverWait(driver, timeout).until(
                EC.invisibility_of_element_located(self.locator)
            )
        except TimeoutException as ex:
            return False

        return True
