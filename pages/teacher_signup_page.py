import allure
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.forms import GoogleSignupForm, WelcomeToTypingPage
from pages.basepage import BasePage
from random import randint


class CompleteYourSignupPage(BasePage):

    def __init__(self, driver: WebDriver, full_name: str):
        super().__init__(driver)
        self.full_name = full_name
        with allure.step("Wait for Complete your signup page to be loaded"):
            self.wait_until_element_located(CompleteYourSignupPageLocator.signup_form)

    @allure.step("Verify `Teacher` form of Complete Your Signup page present")
    def assert_teacher_form_present(self):
        assert self.is_element_present(CompleteYourSignupPageLocator.teacher_form)

    @allure.step("Verify teacher form of Complete Your Signup page is selected")
    def assert_teacher_form_selected(self):
        assert 'is-active' in self.find_element(CompleteYourSignupPageLocator.teacher_form).get_attribute('class')

    @allure.step("Verify `Country` drop down of Complete Your Signup page present")
    def assert_country_drop_down_present(self):
        assert self.is_element_present(CompleteYourSignupPageLocator.country_dropdown)

    @allure.step("Verify `School Name` field of Complete Your Signup page present")
    def assert_school_name_field_present(self):
        assert self.is_element_present(CompleteYourSignupPageLocator.school_name_field)

    @allure.step("Verify `Privacy Police` checkbox of Complete Your Signup page present")
    def assert_privacy_police_checkbox_present(self):
        assert self.is_element_present(CompleteYourSignupPageLocator.privacy_police_checkbox)

    @allure.step("Verify `SignUp` button of Complete Your Signup page present")
    def assert_signup_button_present(self):
        assert self.is_element_present(CompleteYourSignupPageLocator.signup_button)

    @allure.step("Click on the signup button")
    def click_on_signup_button(self) -> WelcomeToTypingPage:
        self.find_element(CompleteYourSignupPageLocator.signup_button).click()
        return WelcomeToTypingPage(self.driver, self.full_name)

    @allure.step("Select '{1}' from country dropdown")
    def select_country_from_country_drop_down(self, country: str):
        country_drop_down: Select = Select(self.find_element(CompleteYourSignupPageLocator.country_dropdown))
        country_drop_down.select_by_visible_text(country)

    @allure.step("Type '{1}' school name into the schoolName field")
    def type_school_name(self, school_name: str):
        self.find_element(CompleteYourSignupPageLocator.school_name_field).send_keys(school_name)

    @allure.step("Select `Privacy Police` checkbox")
    def select_privacy_police_checkbox(self):
        self.find_element(CompleteYourSignupPageLocator.privacy_police_checkbox).click()

    @allure.step("Selected teacher form of Complete Your Signup page")
    def select_teacher_form(self):
        self.find_element(CompleteYourSignupPageLocator.teacher_form).click()
        time.sleep(0.5)


class TeacherSignupPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.page = 'teacher/signup'

    def is_loaded(self):
        try:
            self.wait_until_element_located((By.ID, 'app'))
        except TimeoutError:
            raise RuntimeError(f"The {self.page} page is not loaded properly")

    @allure.step("Verify `Google SignUp` button of Teacher Signup page present")
    def assert_google_signup_button_present(self):
        assert self.is_element_present(TeacherSignupLocator.google_signup_button)

    @allure.step("Verify `Full Name` field of Teacher Signup page present")
    def assert_full_name_field_present(self):
        assert self.is_element_present(TeacherSignupLocator.full_name_field)

    @allure.step("Verify `Email` field of Teacher Signup page present")
    def assert_email_field_present(self):
        assert self.is_element_present(TeacherSignupLocator.email_field)

    @allure.step("Verify `Password` field of Teacher Signup page present")
    def assert_password_field_present(self):
        assert self.is_element_present(TeacherSignupLocator.password_field)

    @allure.step("Verify `Next` button of Teacher Signup page present")
    def assert_next_button_present(self):
        assert self.is_element_present(TeacherSignupLocator.next_button)

    @allure.step("Write '{1}' full name into the FullName field of Teacher Signup page")
    def type_full_name(self, full_name: str):
        self.find_element(TeacherSignupLocator.full_name_field).send_keys(full_name)

    def type_random_email(self) -> str:
        email = f"tester{randint(10, 99)}test{randint(10000, 99999)}@yopmail.com"
        with allure.step(f"Write `{email}` email address into to email field of Teacher Signup page"):
            self.find_element(TeacherSignupLocator.email_field).send_keys(email)
        return email

    @allure.step("Write `{1}` password into the Password field of Teacher Signup page")
    def type_password(self, password: str):
        self.find_element(TeacherSignupLocator.password_field).send_keys(password)

    def click_on_next_button(self) -> CompleteYourSignupPage:
        full_name = self.find_element(TeacherSignupLocator.full_name_field).get_attribute("value")
        self.find_element(TeacherSignupLocator.next_button).click()
        return CompleteYourSignupPage(self.driver, full_name)

    @allure.step("Click on the `Google SignUp` button of Teacher Signup page")
    def click_on_google_signup_button(self) -> GoogleSignupForm:
        self.find_element(TeacherSignupLocator.google_signup_button).click()
        return GoogleSignupForm(self.driver)


class TeacherSignupLocator:
    google_signup_button = (By.XPATH, "//button[@data-action='google-signup']")
    clever_signup_button = (By.XPATH, "//button[@data-action='clever-signup']")
    classlink_signup_button = (By.XPATH, "//button[@data-action='classlink-signup']")
    full_name_field = (By.ID, "form-ele-full_name")
    email_field = (By.ID, "form-ele-email")
    password_field = (By.ID, "form-ele-password")
    show_password_button = (By.XPATH, "//input[@id='form-ele-password']/following-sibling::a[contains(text(),'SHOW')]")
    next_button = (By.XPATH, "//button[contains(text(), 'Next')]")


class CompleteYourSignupPageLocator:
    teacher_form = (By.XPATH, "//div[@data-id='teacher']")
    signup_button = (By.XPATH, "//button[contains(text(), 'Sign Up')]")
    signup_form = (By.ID, "signup-org-form")
    country_dropdown = (By.ID, "form-ele-country")
    school_name_field = (By.ID, "form-ele-name")
    privacy_police_checkbox = (By.ID, "form-ele-tos")
