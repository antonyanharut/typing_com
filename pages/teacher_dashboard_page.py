from random import randint

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.basepage import BasePage
from pages import teacher_classes_page
from pages.teacher_assignment_page import TeacherAssignmentPage
from pages.teacher_classes_page import TeacherClassesPage
from pages.teacher_curriculum_page import TeacherCurriculumPage
from pages.teacher_go_premium_page import LicenseDetailsForm
from pages.teacher_order_page import TeacherOrderPage


class TeacherDashboardPage(BasePage):

    def __init__(self, driver: WebDriver, teacher_name: str):
        super().__init__(driver)
        self.page = 'teacher/dashboard'
        self.teacher_name: str = teacher_name
        with allure.step("Wait until `Teacher Dashboard` page to be loaded."):
            self.wait_until_element_located(TeacherDashboardPageLocator.teacher_name)

    @allure.step("Verify teacher name of Teacher Dashboard page is correct")
    def assert_teacher_name_correct(self):
        current_name = self.find_element(TeacherDashboardPageLocator.teacher_name).text
        assert current_name == self.teacher_name, f"The teacher name is incorrect\n Expected: `{self.teacher_name}` but was `{current_name}`"

    @allure.step("Click on `My Classes` link")
    def click_on_my_classes(self) -> TeacherClassesPage:
        self.click_on_element(TeacherDashboardPageLocator.my_classes)
        return TeacherClassesPage(self.driver)

    @allure.step("Verify `Curriculum` link present")
    def assert_curriculum_present(self):
        assert self.is_element_present(TeacherDashboardPageLocator.curriculum_link), \
            "The `Curriculum` link is missing from the `Teacher Dashboard` page"
        return self

    @allure.step("Verify `Go Premium` button present")
    def assert_go_premium_button_present(self):
        assert self.is_element_present(TeacherDashboardPageLocator.go_premium_button), \
            "The `Go Premium` button is missing from the `Teacher Dashboard` page"

    @allure.step("Verify `Assignments` link present")
    def assert_assignments_present(self):
        assert self.is_element_present(TeacherDashboardPageLocator.assignments_link), \
            "The `Assignments` link is missing from the `Teacher Dashboard` page"
        return self

    @allure.step("Click on `Curriculum` link")
    def click_on_curriculum(self):
        self.click_on_element(TeacherDashboardPageLocator.curriculum_link)
        return TeacherCurriculumPage(self.driver)

    @allure.step("Click on `Assignments` link")
    def click_on_assignments(self):
        self.click_on_element(TeacherDashboardPageLocator.assignments_link)
        return TeacherAssignmentPage(self.driver)

    @allure.step("Click on `Go Premium` button")
    def click_on_go_premium_button(self):
        self.click_on_element(TeacherDashboardPageLocator.go_premium_button)
        return LicenseDetailsForm(self.driver)

    def make_order(self, student_seats='10', term='3', telephone='515454545454', address='Street 1', city='Goris',
                   state='N/A', country='Armenia', zip='3204'):
        with allure.step(
                f"Make order with `{student_seats}` students seats, `{term}` term, {telephone} telephone, {address} address, {city} city, {state} state, {country} country and {zip} zip"):
            self.click_on_go_premium_button() \
                .assert_of_student_seats_field_present() \
                .assert_terms_select_box_present() \
                .assert_continue_to_billing_info_button_present() \
                .type_to_student_seats_field(student_seats) \
                .select_from_term_selectbox(term) \
                .click_on_continue_to_billing_info_button() \
                .assert_address_field_present() \
                .assert_city_field_present() \
                .assert_country_select_box_present() \
                .assert_generate_price_quote_button_present() \
                .assert_state_select_box_present() \
                .assert_telephone_field_present() \
                .assert_zip_code_field_present() \
                .type_telephone_field(telephone) \
                .type_address_field(address) \
                .type_city_field(city) \
                .select_state(state) \
                .select_country(country) \
                .type_zip_code_field(zip) \
                .submit()
            return TeacherOrderPage(self.driver)

    @allure.step("Create a new class with `{1}` name")
    def create_a_new_class(self, class_name: str, function):
        class_page = self.click_on_my_classes()
        class_page.assert_create_a_new_class_button_present()
        class_form = class_page.click_on_create_a_new_class_button()
        class_form.assert_class_name_field_present()
        class_form.assert_create_class_button_present()
        class_form.type_class_name(class_name)
        new_created_class_form = class_form.submit_to_create_class()
        return function(new_created_class_form)

    @allure.step("Click on close button")
    def create_a_new_class_close(self, new_created_class_form):
        new_created_class_form.assert_close_button_present()
        new_created_class_form.click_on_close_button()
        return TeacherClassesPage(self.driver)

    @allure.step("Click on `See My Classes ->` button")
    def create_a_new_class_see_my_classes(self, new_created_class_form):
        new_created_class_form.assert_see_my_classes_button_present()
        new_created_class_form.click_on_see_my_classes_button()
        return TeacherClassesPage(self.driver)

    @allure.step("Click on `Add Students` button")
    def create_a_new_class_add_students(self, new_created_class_form):
        new_created_class_form.assert_add_students_button_present()
        return new_created_class_form.click_on_add_students_button()

class TeacherDashboardPageLocator:
    teacher_name = (By.XPATH, "//div[contains(@class,'mr-3') ]/div[1]")
    my_classes = (By.XPATH, "//li[contains(@data-id,'classes')]")
    curriculum_link = (By.XPATH, "//a[@data-id='curriculum']")
    assignments_link = (By.XPATH, "//a[@data-id='assignments']")
    go_premium_button = (By.XPATH, "//button[@data-tour='click-learn-about-premium']")
