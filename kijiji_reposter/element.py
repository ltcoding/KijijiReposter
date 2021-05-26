from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePageElement(object):
    """Base page class that is initialized on every page object class."""

    TIMEOUT = 10

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

    def click(self, driver):
        try:
            clickable_item = WebDriverWait(driver, ClickableElement.TIMEOUT).until(
                EC.element_to_be_clickable(self.locator)
            )
            clickable_item.click()
        except TimeoutException as ex:
            return False

        return True


class ConfirmationTextElement(BasePageElement):

    def __init__(self, locator):
        super().__init__()
        self.locator = locator

    def confirm(self, driver):
        try:
            WebDriverWait(driver, BasePageElement.TIMEOUT).until(
                EC.presence_of_element_located(self.locator)
            )
        except TimeoutException as ex:
            return False

        return True


