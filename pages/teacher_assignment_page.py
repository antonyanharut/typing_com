import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.basepage import BasePage


class TeacherAssignmentPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.page = 'teacher/assignments'
        with allure.step("Wait until `Teacher Single Class` page to be loaded"):
            self.wait_until_element_is_invisible((By.CLASS_NAME, 'js-loading-animation'))

    @allure.step("Verify the `You Have No Assignments.` text is present on the `Teacher Assignments` page")
    def assert_you_have_no_assignments_text_present(self):
        self.is_element_present(TeacherAssignmentPageLocator.you_have_no_assignments_text), \
        "The `You Have No Assignments.` text is missing from the `Teacher Assignments` page"


class TeacherAssignmentPageLocator:
    you_have_no_assignments_text = (By.XPATH, "//div[text()='You have no assignments.']")
