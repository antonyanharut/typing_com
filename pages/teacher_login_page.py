import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from apis import typing
from pages.basepage import BasePage
from pages.teacher_dashboard_page import TeacherDashboardPage


class TeacherLoginPage(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.page = 'teacher/login'

    def is_loaded(self):
        try:
            self.wait_until_element_located(TeacherLoginPageLocator.email_field)
        except TimeoutError:
            raise RuntimeError(f"The {self.page} page is not loaded properly")

    @allure.step("Verify that `Email` field of `Teacher Login` page is present")
    def assert_email_field_present(self):
        assert self.is_element_present(TeacherLoginPageLocator.email_field), \
            "The `Email` field is missing from the `Teacher Login` page"

    @allure.step("Verify that `Password` field of `Teacher Login` page is present")
    def assert_password_field_present(self):
        assert self.is_element_present(TeacherLoginPageLocator.password_field), \
            "The `Password` field is missing from the `Teacher Login` page"

    @allure.step("Verify that `Next` button of `Teacher Login` page is present")
    def assert_next_button_present(self):
        assert self.is_element_present(TeacherLoginPageLocator.next_button), \
            "The `Next` button is missing from the `Teacher Login` page"

    @allure.step("Verify that `Log In` button of `Teacher Login` page is present")
    def assert_login_button_present(self):
        assert self.is_element_present(TeacherLoginPageLocator.login_button), \
            "The `Login` button is missing from the `Teacher Login` page"

    @allure.step("Write `{1}` email address into the `Email` field of `Teacher Login` page")
    def type_email_address(self, email_address: str):
        self.find_element(TeacherLoginPageLocator.email_field).send_keys(email_address)

    @allure.step("Write `{1}` password into the `Password` field of `Teacher Login` page")
    def type_password(self, password: str):
        self.find_element(TeacherLoginPageLocator.password_field).send_keys(password)

    @allure.step("Click on the `Next` button of `Teacher Login` page")
    def click_on_next_button(self):
        self.find_element(TeacherLoginPageLocator.next_button).click()
        self.wait_until_element_located(TeacherLoginPageLocator.password_field)

    @allure.step("Click on the `Log In` button of `Teacher Login` page")
    def click_on_login_button(self, teacher_name: str = "Test Tester"):
        self.find_element(TeacherLoginPageLocator.login_button).click()
        return TeacherDashboardPage(self.driver, teacher_name)

    def login(self, username=None, password="Tester123") -> TeacherDashboardPage:
        credentials = typing.create_teacher_account()
        with allure.step(f"Login to {credentials['name']}`s account"):
            self.type_email_address(credentials['email'])
            self.click_on_next_button()
            self.type_password(credentials['password'])
            return self.click_on_login_button(teacher_name=credentials['name'])


class TeacherLoginPageLocator():
    email_field = (By.ID, 'form-ele-username')
    password_field = (By.ID, 'form-ele-password')
    next_button = (By.XPATH, "//button[contains(text(),'Next')]")
    login_button = (By.XPATH, "//button[contains(text(),'Log In')]")
