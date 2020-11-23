import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from pages.basepage import BasePage


class BillingInfoForm(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.wait_until_element_located((By.XPATH,
                                         "//h2[text() = 'Billing Contact Info']/ancestor::div[contains(@class,'relative') and contains(@class,'card')]"))

    @allure.step("Verify the `Generate Price Quote` button is present")
    def assert_generate_price_quote_button_present(self):
        assert self.is_element_present(BillingInfoLocator.generate_price_quote_button), \
            "The Generate Price Quote` button is missing from `Billing Info` form"
        return self

    @allure.step("Verify the `Telephone` field is present")
    def assert_telephone_field_present(self):
        assert self.is_element_present(BillingInfoLocator.telephone_field), \
            "The `Telephone` field is missing from `Billing Info` form"
        return self

    @allure.step("Verify the `Address` field is present")
    def assert_address_field_present(self):
        assert self.is_element_present(BillingInfoLocator.address_field), \
            "The `Address` field is missing from `Billing Info` form"
        return self

    @allure.step("Verify the `City` field is present")
    def assert_city_field_present(self):
        assert self.is_element_present(BillingInfoLocator.city_field), \
            "The `City` field is missing from `Billing Info` form"
        return self

    @allure.step("Verify the `Zip Code` field is present")
    def assert_zip_code_field_present(self):
        assert self.is_element_present(BillingInfoLocator.zip_code_field), \
            "The `Zip Code` field is missing from `Billing Info` form"
        return self

    @allure.step("Verify the `State` select box is present")
    def assert_state_select_box_present(self):
        assert self.is_element_present(BillingInfoLocator.state_select_box), \
            "The `State` select box is missing from `Billing Info` form"
        return self

    @allure.step("Verify the `Country` select box is present")
    def assert_country_select_box_present(self):
        assert self.is_element_present(BillingInfoLocator.country_select_box), \
            "The `Country` select box is missing from `Billing Info` form"
        return self

    @allure.step("Type {1} telephone into the `Telephone` field")
    def type_telephone_field(self, telephone):
        self.find_element(BillingInfoLocator.telephone_field).send_keys(telephone)
        return self

    @allure.step("Type {1} address into the `Address` field")
    def type_address_field(self, address):
        self.find_element(BillingInfoLocator.address_field).send_keys(address)
        return self

    @allure.step("Type {1} city into the `City` field")
    def type_city_field(self, city):
        self.find_element(BillingInfoLocator.city_field).send_keys(city)
        return self

    @allure.step("Type {1} zip code into the `Zip Code` field")
    def type_zip_code_field(self, zip):
        self.find_element(BillingInfoLocator.zip_code_field).send_keys(zip)
        return self

    @allure.step("Select {1} from the `State` select box")
    def select_state(self, state):
        Select(self.find_element(BillingInfoLocator.state_select_box)).select_by_visible_text(state)
        return self

    @allure.step("Select {1} from the `Country` select box")
    def select_country(self, country):
        Select(self.find_element(BillingInfoLocator.country_select_box)).select_by_visible_text(country)
        return self

    @allure.step("Submit")
    def submit(self):
        self.find_element(BillingInfoLocator.zip_code_field).submit()
        # self.wait_until_element_located((By.CLASS_NAME, 'js-loading-animation'))
        self.wait_until_url_contains("teacher/order")


class LicenseDetailsForm(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.wait_until_element_located((By.XPATH,
                                         "//h2[text() = 'License Details']/ancestor::div[contains(@class,'relative') and contains(@class,'card')]"))

    @allure.step("Verify the `Term(In Years)` select box is present")
    def assert_terms_select_box_present(self):
        assert self.is_element_present(LicenseDetailsLocator.term_selectbox), \
            "The `Term(In Years)` select box is missing from the `License Details` form"
        return self

    @allure.step("Verify the `of Student Seats` field is present")
    def assert_of_student_seats_field_present(self):
        assert self.is_element_present(LicenseDetailsLocator.students_seats_field), \
            "The `of Student Seats` field is missing from the `License Details` form"
        return self

    @allure.step("Verify the `Continue To Billing Info` button is present")
    def assert_continue_to_billing_info_button_present(self):
        assert self.is_element_present(LicenseDetailsLocator.continue_to_billing_info_button), \
            "The `Continue To Billing Info` button is missing from the `License Details` form"
        return self

    @allure.step("Type {1} seats count into the `of Student Seats` field")
    def type_to_student_seats_field(self, seats):
        field = self.find_element(LicenseDetailsLocator.students_seats_field)
        field.clear()
        field.send_keys(seats)
        return self

    @allure.step("Select {1} from the `Term(In Year)` select box")
    def select_from_term_selectbox(self, value):
        Select(self.find_element(LicenseDetailsLocator.term_selectbox)).select_by_value(value)
        return self

    @allure.step("Click on `Continue To Billing Info` button")
    def click_on_continue_to_billing_info_button(self) -> BillingInfoForm:
        self.click_on_element(LicenseDetailsLocator.continue_to_billing_info_button)
        self.wait_until_element_is_invisible(LicenseDetailsLocator.continue_to_billing_info_button)
        return BillingInfoForm(self.driver)


class LicenseDetailsLocator:
    students_seats_field = (By.ID, "form-ele-quantity_annual")
    term_selectbox = (By.ID, "form-ele-term")
    continue_to_billing_info_button = (
        By.XPATH, "//button[contains(@class, 'js-submit') and contains(text(), 'Continue to Billing')]")


class BillingInfoLocator:
    telephone_field = (By.ID, "form-ele-phone")
    address_field = (By.ID, "form-ele-address1")
    city_field = (By.ID, "form-ele-city")
    state_select_box = (By.ID, "form-ele-state")
    country_select_box = (By.ID, "form-ele-country")
    zip_code_field = (By.ID, "form-ele-postal")
    generate_price_quote_button = (By.XPATH, "//button[contains(text(),'Generate Price Quote')]")
