import os
import time

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.basepage import BasePage


class TeacherCurriculumPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.page = 'teacher/curriculum'
        with allure.step("Wait until `Teacher Single Class` page to be loaded"):
            self.wait_until_element_is_invisible((By.CLASS_NAME, 'js-loading-animation'))
            self.wait_until_element_located((By.XPATH, "//h1[text() = 'Curriculum']"))

    @allure.step("Verify the `Create/View Lesson` button present")
    def assert_lesson_button_present(self):
        self.is_element_present(TeacherCurriculumPageLocator.lessons_button), \
        "The `Create/View Lesson` button is missing from the `Teacher Curriculum` page"
        return self

    @allure.step("Verify the `Create/View Test` button present")
    def assert_test_button_present(self):
        self.is_element_present(TeacherCurriculumPageLocator.lessons_button), \
        "The `Create/View Test` button is missing from the `Teacher Curriculum` page"
        return self

    @allure.step("Verify the text of `Create/View Lesson` button is {1}")
    def assert_text_of_lesson_button(self, expected_text):
        actual_text = self.text_of(TeacherCurriculumPageLocator.lessons_button).strip()
        assert actual_text == expected_text, \
            f"The text of `Create/View Lesson` button is `{actual_text}` but expected to be `{expected_text}`"
        return self

    @allure.step("Verify the text of `Create/View Test` button is {1}")
    def assert_text_of_test_button(self, expected_text):
        actual_text = self.text_of(TeacherCurriculumPageLocator.tests_button).strip()
        assert actual_text == expected_text, \
            f"The text of `Create/View Test` button is `{actual_text}` but expected to be `{expected_text}`"
        return self

    @allure.step("Wait for success checkbox to be located")
    def wait_until_success(self):
        try:
            self.wait_until_element_located((By.XPATH, '//div[contains(@class, "notice--success")]'))
        except TimeoutException:
            assert False, \
                "The added successfully checkbox is missing"

    @allure.step("Click on the `Create/View Lesson` button")
    def click_on_lessons_button(self):
        self.click_on_element(TeacherCurriculumPageLocator.lessons_button)

    @allure.step("Click on the `Create/View Test` button")
    def click_on_test_button(self):
        if os.environ['BROWSER'] == 'safari':
            self.driver.execute_script("arguments[0].click()",
                                       self.find_element(TeacherCurriculumPageLocator.tests_button))
        else:
            self.click_on_element(TeacherCurriculumPageLocator.tests_button)

    def create_custom_lesson(self, lesson_title="Test", typing_content="Test Content"):
        with allure.step(f"Create custom lesson with `{lesson_title}` title and `{typing_content}` typing content"):
            self.assert_lesson_button_present() \
                .assert_text_of_lesson_button("Create Custom Lesson") \
                .click_on_lessons_button()
            lesson_form = CreateACustomLessonForm(self.driver)
            lesson_form.assert_lesson_title_field_present()
            lesson_form.assert_typing_content_field_present()
            lesson_form.assert_create_custom_lesson_button_present()
            lesson_form.type_title_field(lesson_title)
            lesson_form.type_typing_content_field(typing_content)
            lesson_form.submit_to_create_custom_lesson()
            self.wait_until_success()
        return self

    def create_custom_test(self, test_title="Test", test_screen_content="Test Content"):
        with allure.step(
                f"Create custom test with `{test_title}` title and `{test_screen_content}` test screen content"):
            self.assert_test_button_present().assert_text_of_test_button(
                'Create Custom Timed Test').click_on_test_button()
            test_form = CreateACustomTestForm(self.driver)
            test_form.assert_typing_test_title_field_present()
            test_form.assert_test_screen_content_field_present()
            test_form.assert_create_a_custom_timed_test_present()
            test_form.type_title_field(test_title)
            test_form.type_typing_content_field(test_screen_content)
            test_form.submit_to_create_custom_timed_test()
            self.wait_until_success()
        return self


class CreateACustomLessonForm(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.wait_until_element_located(CreateACustomLessonLocator.lesson_title_field)

    @allure.step("Verify the `Lesson Title` field is present")
    def assert_lesson_title_field_present(self):
        assert self.is_element_present(CreateACustomLessonLocator.lesson_title_field), \
            "The `Lesson Title` field is missing from the `Create A Custom Lesson` filed"

    @allure.step("Verify the `Typing Content` field is present")
    def assert_typing_content_field_present(self):
        assert self.is_element_present(CreateACustomLessonLocator.typing_content_field), \
            "The `Typing Content` field is missing from the `Create A Custom Lesson` filed"

    @allure.step("Verify the `Create Custom Lesson` button is present")
    def assert_create_custom_lesson_button_present(self):
        assert self.is_element_present(CreateACustomLessonLocator.create_custom_lesson_button), \
            "The `Create Custom Lesson` button is missing from the `Create A Custom Lesson` form"

    @allure.step("Type {1} title into the `Lesson Title` field")
    def type_title_field(self, title):
        self.find_element(CreateACustomLessonLocator.lesson_title_field).send_keys(title)

    @allure.step("Type {1} content into the `Typing Content` field")
    def type_typing_content_field(self, content):
        self.find_element(CreateACustomLessonLocator.typing_content_field).send_keys(content)

    @allure.step("Submit to create custom lesson")
    def submit_to_create_custom_lesson(self):
        self.find_element(CreateACustomLessonLocator.lesson_title_field).submit()


class CreateACustomTestForm(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.wait_until_element_located(CreateACustomTestLocator.typing_test_title_field)

    @allure.step("Verify the `Typing Test Title` field is present")
    def assert_typing_test_title_field_present(self):
        assert self.is_element_present(CreateACustomTestLocator.typing_test_title_field), \
            "The `Typing Test Title` field is missing from the `Create A Custom Test"

    @allure.step("Verify the `Test Screen Content` field is present")
    def assert_test_screen_content_field_present(self):
        assert self.is_element_present(CreateACustomTestLocator.test_screen_content_field), \
            "The `Test Screen Content` field is missing from the `Create A Custom Test"

    @allure.step("Verify the `Custom Timed Test` button is present")
    def assert_create_a_custom_timed_test_present(self):
        assert self.is_element_present(CreateACustomTestLocator.create_custom_timed_test_button), \
            "The `Custom Timed Test` button is missing from the `Create A Custom Test"

    @allure.step("Type {1} title into the `Typing Test Title` field")
    def type_title_field(self, title):
        self.find_element(CreateACustomTestLocator.typing_test_title_field).send_keys(title)

    @allure.step("Type {1} content into the `Test Screen Content` field")
    def type_typing_content_field(self, content):
        self.find_element(CreateACustomTestLocator.test_screen_content_field).send_keys(content)

    @allure.step("Submit create custom timed test")
    def submit_to_create_custom_timed_test(self):
        self.find_element(CreateACustomTestLocator.typing_test_title_field).submit()


class CreateACustomLessonLocator:
    lesson_title_field = (By.ID, "form-ele-lesson_name")
    typing_content_field = (By.ID, "form-ele-content")
    create_custom_lesson_button = (By.XPATH, "//div/button[contains(text(),'Create Custom Lesson')]")


class CreateACustomTestLocator:
    typing_test_title_field = (By.ID, "form-ele-lesson_name")
    test_screen_content_field = (By.ID, "form-ele-content")
    create_custom_timed_test_button = (By.XPATH, "//button[contains(text(),'Create') and not(contains(text(),'How'))]")


class TeacherCurriculumPageLocator:
    lessons_button = (By.XPATH, "//div[@data-unit-type='lesson']//button[not(contains(text(),'How'))]")
    tests_button = (By.XPATH, "//div[@data-unit-type='test']//button[not(contains(text(),'How'))]")
