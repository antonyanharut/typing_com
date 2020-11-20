import time
from random import randint

import allure
import pytest

from apis.typing import delete_teacher_using_cache
from pages.teacher_classes_page import SingleClassPage
from pages.teacher_login_page import TeacherLoginPage


@allure.feature("Teacher")
@pytest.mark.usefixtures("get_driver")
class TestTeacherClassesPage:

    def setup(self):
        self.login = TeacherLoginPage(self.driver)
        self.login.get()
        self.page = self.login.login()

    @allure.testcase(
        'A35:F35',
        'CS_1')
    @allure.title(
        'With zero students in your class, click the "Add Students" button in the middle of the page. Add a single student')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Class Students")
    @pytest.mark.class_students
    def test_add_a_single_student(self):
        username = f"tester{randint(10, 99)}test{randint(1000, 9999)}"
        self.page.create_a_new_class('Hello') \
            .click_on_class('Hello') \
            .click_on_add_students_button() \
            .create_a_new_student(username)
        SingleClassPage(self.driver) \
            .assert_students_tab_present() \
            .assert_students_count_is(1) \
            .assert_student_with_username_present(username)
        delete_teacher_using_cache(self.driver)

    @allure.testcase(
        'A54:G54',
        'CA_1')
    @allure.title(
        'From the assignments tab on the class page, click "Add Assignment" and create a new Lessons Assignment. Assign it to one class')
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Class Assignments")
    @allure.issue('13:13', "[Teacher] A long description gets out of the assignment summary window")
    @pytest.mark.class_assignments
    def test_add_a_new_lesson_assignment(self):
        self.page.create_a_new_class('Hello') \
            .click_on_class('Hello') \
            .click_on_assignments_tab() \
            .click_on_add_assignment_button() \
            .create_typing_lessons_assignment()
        SingleClassPage(self.driver) \
            .assert_assignments_tab_present() \
            .assert_assignments_tab_count_is(1)
        delete_teacher_using_cache(self.driver)

    @allure.testcase(
        'A55:G55',
        'CA_2')
    @allure.title(
        'From the assignments tab on the class page, click "Add Assignment" and create a new Written Prompt Assignment. Assign it to one class')
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Class Assignments")
    @allure.issue('13:13', "[Teacher] A long description gets out of the assignment summary window")
    @pytest.mark.class_assignments
    def test_add_a_written_prompt_assignment(self):
        self.page.create_a_new_class('Hello') \
            .click_on_class('Hello') \
            .click_on_assignments_tab() \
            .click_on_add_assignment_button() \
            .create_written_prompt_assignment()
        SingleClassPage(self.driver) \
            .assert_assignments_tab_present() \
            .assert_assignments_tab_count_is(1)
        delete_teacher_using_cache(self.driver)

    @allure.title(
        'From the assignments tab on the class page, click "Add Assignment" and create a new Lessons Assignment. Assign it to multiple classes')
    @allure.testcase('A57:G57', name='CA_4')
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Class Assignments")
    @allure.issue('13:13', "[Teacher] A long description gets out of the assignment summary window")
    @pytest.mark.class_assignments
    def test_add_a_lesson_assignment_for_multiple_classes(self):
        self.page.create_a_new_class('Test1')
        time.sleep(0.5)
        self.page.create_a_new_class('Test2') \
            .click_on_class('Test1') \
            .click_on_assignments_tab() \
            .click_on_add_assignment_button() \
            .create_typing_lessons_assignment(classes="Test2", title='TestAssignment')
        SingleClassPage(self.driver) \
            .assert_my_classes_link_present() \
            .assert_assignments_tab_present() \
            .assert_assignments_tab_count_is(1) \
            .assert_assignment_by_name_present('TestAssignment') \
            .click_on_my_classes_link().click_on_class('Test2') \
            .click_on_assignments_tab() \
            .assert_assignments_tab_count_is(1) \
            .assert_assignment_by_name_present('TestAssignment')

    @allure.title(
        'From the assignments tab on the class page, click "Add Assignment" and create a new Tests Assignment. Assign it to any number of students within your class')
    @allure.testcase('A56:G56', name='CA_3')
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Class Assignments")
    @allure.issue('13:13', "[Teacher] A long description gets out of the assignment summary window")
    @pytest.mark.class_assignments
    def test_add_assignment_with_multiple_students(self):
        username = f"tester{randint(10, 99)}test{randint(1000, 9999)}"
        username1 = f"tester{randint(10, 99)}test{randint(1000, 9999)}"
        self.page.create_a_new_class('Hello') \
            .click_on_class('Hello') \
            .click_on_add_students_button() \
            .create_a_new_student((username, username1))
        SingleClassPage(self.driver) \
            .refresh_page() \
            .click_on_assignments_tab() \
            .click_on_add_assignment_button() \
            .create_typing_assessment_assignment(title='TestAssignment', students=(username, username1),
                                                 lessons="1 Page Typing Test")
        SingleClassPage(self.driver) \
            .assert_assignments_tab_present() \
            .assert_assignments_tab_count_is(1) \
            .assert_assignment_by_name_present('TestAssignment')
