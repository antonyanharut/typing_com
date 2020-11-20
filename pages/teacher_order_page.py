import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.basepage import BasePage


class TeacherOrderPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.page = 'teacher/order'
        self.wait_until_element_is_invisible((By.CLASS_NAME, 'js-loading-animation'))
        self.wait_until_element_located((By.XPATH, "//h1[text() = 'Price Quote']"))

    @allure.step("Verify the `Start Date Of Payment` present")
    def assert_start_date_of_payment_present(self):
        assert self.is_element_present(TeacherOrderLocator.start_date_of_payment), \
            "The `Start Date Of Payment` is missing from the `Teacher Order` page"
        return self

    @allure.step("Verify the `# Student Seats` present")
    def assert_student_seats_present(self):
        assert self.is_element_present(TeacherOrderLocator.student_seats), \
            "The `# Student Seats` is missing from the `Teacher Order` page"
        return self

    @allure.step("Verify the `Term` present")
    def assert_term_present(self):
        assert self.is_element_present(TeacherOrderLocator.term), \
            "The `Term` is missing from the `Teacher Order` page"
        return self

    @allure.step("Verify the text of `Start Date Of Payment` is {1}")
    def assert_text_of_start_date_of_payment(self, expected_text):
        actual_text = self.text_of(TeacherOrderLocator.start_date_of_payment).strip()
        assert actual_text == expected_text, \
            f"The text of `Start Date Of Payment` expected to be `{expected_text}` but was `{actual_text}`"
        return self

    @allure.step("Verify the text of `# Student Seats` is {1}")
    def assert_text_of_student_seats(self, expected_text):
        actual_text = self.text_of(TeacherOrderLocator.student_seats).strip()
        assert actual_text == expected_text, \
            f"The text of `# Student Seats` expected to be `{expected_text}` but was `{actual_text}`"
        return self

    @allure.step("Verify the text of `Term` is {1}")
    def assert_text_of_term(self, expected_text):
        actual_text = self.text_of(TeacherOrderLocator.term).strip()
        assert actual_text == expected_text, \
            f"The text of `Term` expected to be `{expected_text}` but was `{actual_text}`"
        return self


class TeacherOrderLocator:
    start_date_of_payment = (By.XPATH, "//table[contains(@class,'table--striped')]/tbody/tr[1]/td[4]")
    student_seats = (By.XPATH, "//table[contains(@class,'table--striped')]/tbody/tr[1]/td[2]")
    term = (By.XPATH, "//table[contains(@class,'table--striped')]/tbody/tr[1]/td[3]")
