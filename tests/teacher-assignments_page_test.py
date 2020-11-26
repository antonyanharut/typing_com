import allure
import pytest

from pages.teacher_login_page import TeacherLoginPage


@allure.story("Assignments")
@allure.feature("Teacher")
@pytest.mark.usefixtures("get_driver")
class TestTeacherAssignmentsPage:

    def setup(self):
        self.login = TeacherLoginPage(self.driver)
        self.login.get()
        self.page = self.login.login().click_on_assignments()

    @allure.testcase(
        'A96:F96',
        'A_1')
    @allure.title(
        'With no assignments, the page should show a message saying you have no assignments')
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.assignments
    def test_no_assignments(self):
        self.page.assert_you_have_no_assignments_text_present()
