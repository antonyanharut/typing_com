import time

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from credentials.google.google_credentials import name
from pages.teacher_dashboard_page import TeacherDashboardPage
from pages.basepage import BasePage


class GoogleSignupForm(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step("Write '{1}' email address into the email field of google signup form")
    def __type_email(self, email_address: str):
        self.wait_until_element_located(GoogleSignupFormLocator.google_email_field)
        email_field = self.find_element(GoogleSignupFormLocator.google_email_field)
        email_field.send_keys(email_address)
        email_field.send_keys(Keys.ENTER)
        self.wait_until_element_located(GoogleSignupFormLocator.google_password_field)

    @allure.step("Write '{1}' password into the password field of google signup form")
    def __type_password(self, password: str):
        self.wait_until_element_located(GoogleSignupFormLocator.google_password_field)
        email_field = self.find_element(GoogleSignupFormLocator.google_password_field)
        email_field.send_keys(password)
        email_field.send_keys(Keys.ENTER)

    @allure.step("Signup with google account")
    def signup(self):
        from pages.teacher_signup_page import CompleteYourSignupPage
        from credentials.google.google_credentials import email
        from credentials.google.google_credentials import password

        self.__type_email(email())
        self.__type_password(password())
        try:
            self.wait_until_element_located(GoogleSignupFormLocator.allow_access_button, time_out=3)
            self.find_element(GoogleSignupFormLocator.allow_access_button).click()
        except TimeoutException:
            pass
        return CompleteYourSignupPage(self.driver, name())


class WelcomeToTypingPage(BasePage):

    def __init__(self, driver: WebDriver, name: str):
        super().__init__(driver)
        self.name = name
        with allure.step("Wait for `Welcome To Typing.com` page to be loaded."):
            self.wait_until_element_located(WelcomeToTypingPageLocator.welcome_form)

    @allure.step("Verify `Cancel` button of Welcome To Typing.com form present")
    def assert_cancel_button_present(self):
        assert self.is_element_present(WelcomeToTypingPageLocator.cancel_button)

    @allure.step("Click on `Cancel` button of Welcome To Typing.com form")
    def click_on_cancel_button(self) -> TeacherDashboardPage:
        self.find_element(WelcomeToTypingPageLocator.cancel_button).click()
        return TeacherDashboardPage(self.driver, self.name)


class GoogleSignupFormLocator:
    google_email_field = (By.XPATH, "//input[@autocomplete='username']")
    google_password_field = (By.XPATH, "//input[@autocomplete='current-password']")
    allow_access_button = (By.ID, 'submit_approve_access')


class WelcomeToTypingPageLocator:
    welcome_form = (By.XPATH, "//div[contains(@class,'items-start')]")
    cancel_button = (By.XPATH, "//button[contains(text(),'Cancel')]")
