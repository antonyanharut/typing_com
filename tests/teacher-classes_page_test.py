import time
from random import randint

import allure
import pytest

from apis.typing import delete_teacher_using_cache
from helpers import generate_random_email
from pages.teacher_classes_page import SingleClassPage, TeacherClassesPage, DeleteClassDialog
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
        username = generate_random_email()
        self.page.create_a_new_class('Hello', self.page.create_a_new_class_close) \
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
        self.page.create_a_new_class('Hello', self.page.create_a_new_class_close) \
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
        self.page.create_a_new_class('Hello', self.page.create_a_new_class_close) \
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
        self.page.create_a_new_class('Test1', self.page.create_a_new_class_close)
        time.sleep(0.5)
        self.page.create_a_new_class('Test2', self.page.create_a_new_class_close) \
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
        username = generate_random_email()
        username1 = generate_random_email()
        self.page.create_a_new_class('Hello', self.page.create_a_new_class_close) \
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

    @allure.testcase(
        'A19:F19',
        'CLSS_1')
    @allure.title(
        'With zero classes, create a class using the "Create a new Class" button in the middle of the page. When asked to add students, say no')
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Classes")
    @pytest.mark.classes
    def test_add_class_without_students(self):
        self.page.create_a_new_class('Hello', self.page.create_a_new_class_see_my_classes) \
            .assert_first_class_present() \
            .assert_first_class_title('Hello')
        delete_teacher_using_cache(self.driver)

    @allure.testcase(
        'A20:F20',
        'CLSS_2')
    @allure.title(
        'With zero classes, create a class using the "Create a new Class" button in the middle of the page. When asked to add students, click "add students" and add a single student')
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Classes")
    @pytest.mark.classes
    def test_add_class_add_students(self):
        username = generate_random_email()
        self.page.create_a_new_class('Hello', self.page.create_a_new_class_add_students) \
            .create_a_new_student(username)
        TeacherClassesPage(self.driver)\
            .click_on_class('Hello')
        SingleClassPage(self.driver) \
            .assert_students_tab_present() \
            .assert_students_count_is(1) \
            .assert_student_with_username_present(username)
        delete_teacher_using_cache(self.driver)


    @allure.testcase(
        'A21:F21',
        'CLSS_3')
    @allure.title(
        'Select a class with students and attempt to delete it using the "bulk actions" delete option')
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Classes")
    @pytest.mark.classes
    def test_delete_class_with_students(self):
        username = generate_random_email()
        self.page.create_a_new_class('Hello', self.page.create_a_new_class_add_students) \
            .create_a_new_student(username)
        TeacherClassesPage(self.driver)\
            .assert_bulk_actions_present().select_class_with_name('Hello').select_delete_from_bulk_actions()\
            .assert_delete_class_error_present().assert_delete_class_error_contains("You can not delete classes which contain students")



    @allure.testcase(
        'A22:F22',
        'CLSS_4')
    @allure.title(
        'Select 1 or more classes that do not have students and delete them using the "bulk actions" delete option')
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Classes")
    @pytest.mark.classes
    def test_delete_class_without_students(self):
        self.page.create_a_new_class('Hello', self.page.create_a_new_class_see_my_classes)
        TeacherClassesPage(self.driver)\
            .assert_bulk_actions_present().select_class_with_name('Hello').select_delete_from_bulk_actions()
        DeleteClassDialog(self.driver)\
        .assert_confirm_text_field_present()\
        .confirm().assert_class_missing('Hello')