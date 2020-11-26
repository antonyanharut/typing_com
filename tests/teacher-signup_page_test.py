import allure
import pytest

from pages.forms import WelcomeToTypingPage
from pages.teacher_dashboard_page import TeacherDashboardPage
from pages.teacher_signup_page import TeacherSignupPage, CompleteYourSignupPage
from apis.typing import delete_teacher_using_cache


@allure.step("Validate `Welcome To Typing.com` page")
def welcome_to_typing_click_on_cancel_button(page: WelcomeToTypingPage) -> TeacherDashboardPage:
    page.assert_cancel_button_present()
    return page.click_on_cancel_button()


@allure.step("Validate user navigates to correct `Teacher Dashboard` page")
def validate_teacher_dashboard_page_is_correct(page: TeacherDashboardPage):
    with allure.step(f"Verify the page url is `{page.correct_url()}`"):
        assert page.at_page(), f"After `Teacher Signup` the user is redirected to `{page.current_url()}`" \
                               f", but expected url is `{page.correct_url()}`"
    page.assert_teacher_name_correct()


def complete_signup(complete_your_signup_page: CompleteYourSignupPage):
    with allure.step("Validate `Complete Signup` page"):
        complete_your_signup_page.assert_signup_button_present()
        complete_your_signup_page.assert_teacher_form_present()
        complete_your_signup_page.select_teacher_form()
        complete_your_signup_page.assert_teacher_form_selected()
        complete_your_signup_page.assert_country_drop_down_present()
        complete_your_signup_page.assert_school_name_field_present()
        complete_your_signup_page.assert_privacy_police_checkbox_present()
        complete_your_signup_page.select_country_from_country_drop_down("Armenia")
        complete_your_signup_page.type_school_name('School N5')
        complete_your_signup_page.select_privacy_police_checkbox()

    teacher_dashboard: TeacherDashboardPage = welcome_to_typing_click_on_cancel_button(
        complete_your_signup_page.click_on_signup_button())
    validate_teacher_dashboard_page_is_correct(teacher_dashboard)


@allure.feature("Teacher")
@allure.story("Signup")
@pytest.mark.usefixtures("get_driver")
class TestTeacherSignupPage:

    def setup(self):
        self.teacher_signup_page: TeacherSignupPage = TeacherSignupPage(self.driver)
        self.teacher_signup_page.get()

    @allure.testcase(
        'A3:F3',
        'SU_1')
    @allure.title('Sign up using Google - create a TEACHER account')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.signup
    @pytest.mark.teacher_signup
    def test_signup_with_google(self):
        self.teacher_signup_page.assert_google_signup_button_present()
        # Complete Your Signup page
        complete_signup(self.teacher_signup_page.click_on_google_signup_button().signup())
        delete_teacher_using_cache(self.driver)

    @allure.testcase(
        'A4:F4',
        'SU_2')
    @allure.title('Sign up using Username/Password - create a TEACHER account')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.signup
    @pytest.mark.teacher_signup
    def test_signup_with_username_password(self):
        self.teacher_signup_page.get()
        self.teacher_signup_page.assert_full_name_field_present()
        self.teacher_signup_page.assert_email_field_present()
        self.teacher_signup_page.assert_password_field_present()
        self.teacher_signup_page.assert_next_button_present()
        self.teacher_signup_page.type_full_name("Tester Test")
        self.teacher_signup_page.type_random_email()
        self.teacher_signup_page.type_password("Tester#123")
        complete_signup(self.teacher_signup_page.click_on_next_button())
        delete_teacher_using_cache(self.driver)
