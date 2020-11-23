import os
import time

import allure

from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    ElementNotInteractableException, ElementClickInterceptedException, ElementNotVisibleException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver
        self.page = ''
        self.wait_action = wait = WebDriverWait(driver, 20, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, NoSuchElementException,ElementNotInteractableException])

    def correct_url(self) -> str:
        return f"{os.environ.get('URL')}/{self.page}"

    def current_url(self) -> str:
        return self.driver.current_url

    def load(self):
        with allure.step(f"Load the '{self.page}' page."):
            self.driver.get(self.correct_url())

    def is_loaded(self):
        if not self.at_page():
            raise RuntimeError(f"The {self.page} page is not loaded properly")

    def get(self):
        try:
            if not self.at_page():
                self.load()
            self.is_loaded()
        except RuntimeError:
            self.load()
            self.is_loaded()
        return self

    def at_page(self) -> bool:
        return self.current_url() == self.correct_url()

    def text_of(self,locator):
        is_stale = True
        text = ''
        while is_stale:
            try:
                text = self.find_element(locator).text
                is_stale = False
            except StaleElementReferenceException:
                print(locator)
                time.sleep(0.1)
        return text

    @allure.step("Wait until {1} element to be located")
    def wait_until_element_located(self, locator, time_out: int = 20):
        try:
            WebDriverWait(self.driver, time_out).until(
                EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"The {locator} element is not located after {time_out} seconds of wait")

    @allure.step("Wait until {1} element to be invisible")
    def wait_until_element_is_invisible(self, locator, time_out: int = 20):
        try:
            WebDriverWait(self.driver, time_out).until(
                EC.invisibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"The {locator} element is not invisible after {time_out} seconds of wait")

    @allure.step("Wait until the page url contains {1}")
    def wait_until_url_contains(self, url, time_out: int = 20):
        try:
            WebDriverWait(self.driver,time_out).until(EC.url_contains(url))
        except TimeoutException:
            raise TimeoutException(f"After {time_out} seconds of wait the page url doens't contain {url}")

    # StaleElementReferenceException
    def click_on_element(self, locator):
        # self.driver.execute_script("arguments[0].scrollIntoView()", self.find_element(locator))
        is_stale = True
        while is_stale:
            try:
                self.wait_action.until(EC.element_to_be_clickable(locator)).click()
                is_stale = False
            except StaleElementReferenceException:
                print(locator)
                time.sleep(0.1)
            except (ElementNotInteractableException, ElementClickInterceptedException):
                #firefox solution
                element = self.find_element(locator)
                ActionChains(self.driver).move_to_element(element).click(element).perform()
                time.sleep(1)
                is_stale = False



    def find_element(self, locator) -> WebElement:
        element = self.driver.find_element(*locator)
        is_stale = True
        while is_stale:
            try:
                element = self.driver.find_element(*locator)
                element.is_displayed()
                is_stale = False
            except StaleElementReferenceException:
                time.sleep(0.1)
        return element

    @allure.step("Checking {1} element is present")
    def is_element_present(self, locator) -> bool:
        try:
            self.find_element(locator)
            return True
        except NoSuchElementException:
            return False
        except StaleElementReferenceException:
            WebDriverWait(self.driver, 5).until(EC.staleness_of(locator))
            return True

    def refresh_page(self):
        self.driver.refresh()