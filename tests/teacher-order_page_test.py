import allure
import pytest
from pages.teacher_login_page import TeacherLoginPage


@allure.story("Upgrade")
@allure.feature("Teacher")
@pytest.mark.usefixtures("get_driver")
class TestTeacherCurriculumPage:

    def setup(self):
        self.login = TeacherLoginPage(self.driver)
        self.login.get()
        self.page = self.login.login()

    @allure.testcase(
        'A88:F88',
        'A119:F119')
    @allure.title(
        '''Click "Go Premium!" on the top of the page. Choose the following:
- 10 seats
- 3 year
- No start date
- Enter anything for the Billing Contact Info
Generate the price quote''')
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.upgrade
    def test_make_order(self):
        self.page.make_order().assert_start_date_of_payment_present() \
            .assert_start_date_of_payment_present() \
            .assert_term_present() \
            .assert_text_of_start_date_of_payment('Upon Payment') \
            .assert_text_of_student_seats('10') \
            .assert_text_of_term('3 Years')
