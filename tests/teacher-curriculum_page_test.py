import allure
import pytest
from pages.teacher_login_page import TeacherLoginPage


@allure.story("Curriculum")
@allure.feature("Teacher")
@pytest.mark.usefixtures("get_driver")
class TestTeacherCurriculumPage:

    def setup(self):
        self.login = TeacherLoginPage(self.driver)
        self.login.get()
        self.page = self.login.login().click_on_curriculum()

    @allure.testcase(
        'A88:F88',
        'CR_1a')
    @allure.title(
        'Click "Create a custom lesson" button. Fill out the form and create a new custom lesson.')
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.curriculum
    def test_create_custom_lesson(self):
        self.page.create_custom_lesson().assert_text_of_lesson_button("View 1 Lesson ›")

    @allure.testcase(
        'A93:F93',
        'CR_5a')
    @allure.title(
        'Click "Create a custom test" button. Fill out the form and create a new custom test.')
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.curriculum
    def test_create_custom_test(self):
        self.page.create_custom_test().assert_text_of_test_button("View 1 Test ›")
