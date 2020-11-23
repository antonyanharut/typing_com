import os
import re

import allure
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.support.wait import WebDriverWait

from pages.basepage import BasePage


class AddStudentsForm(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        with allure.step("Wait `Add Students` form to be located."):
            self.wait_until_element_located((By.XPATH,
                                             "//h3[contains(text(),'Add Students')]"))

    @allure.step("Verify the `Add Single Student` of `Add Students` page present")
    def assert_add_single_student_present(self):
        assert self.is_element_present(AddStudentsLocator.add_single_student_form), \
            "The `Add Single Student` is missing from the `Add Students` form"

    @allure.step("Verify the `Create Single Student` button of `Add Students` form present")
    def assert_create_single_student_button_present(self):
        assert self.is_element_present(AddStudentsLocator.create_single_student_button), \
            "The `Create Single Student` button is missing from the `Add Students` form"

    @allure.step("Verify the `Username` field of `Add Students` form present")
    def assert_username_field_present(self):
        assert self.is_element_present(AddStudentsLocator.username_field), \
            "The `Username` field is missing from the `Add Students` form"

    @allure.step("Verify the `Passowrd` field of `Add Students` form present")
    def assert_password_field_present(self):
        assert self.is_element_present(AddStudentsLocator.password_field), \
            "The `Password` field is missing from the `Add Students` form"

    @allure.step("Verify the `Close` button of `Add Students` form present")
    def assert_close_button_present(self):
        assert self.is_element_present(AddStudentsLocator.close_button), \
            "The `Close` button is missing from the `Add Students` form"

    @allure.step("Select `Add Single Student` from the `Add Students` form")
    def select_add_single_student_button(self):
        self.click_on_element(AddStudentsLocator.add_single_student_form)
        time.sleep(0.3)

    @allure.step("Write `{1}` username into the `Username` field of `Add Students` form")
    def type_username(self, username: str):
        self.find_element(AddStudentsLocator.username_field).send_keys(username)

    @allure.step("Write `{1}` passowrd into the `Password` field of `Add Students` form")
    def type_password(self, password: str):
        self.find_element(AddStudentsLocator.password_field).send_keys(password)

    @allure.step("Submit")
    def submit_to_create_a_student(self):
        self.find_element(AddStudentsLocator.password_field).submit()

    @allure.step("Click on `Close` button of `Add Students` form")
    def click_on_close_button(self):
        self.click_on_element(AddStudentsLocator.close_button)

    @allure.step("Wait until student to be added")
    def assert_student_added_successfully(self):
        try:
            self.wait_until_element_located(AddStudentsLocator.student_added_success)
        except TimeoutException:
            assert False, \
                'The `Student added success` form is missing'

    @allure.step("Add a new student with {1} username")
    def create_a_new_student(self, username):
        self.assert_add_single_student_present()
        self.select_add_single_student_button()
        self.assert_create_single_student_button_present()
        self.assert_username_field_present()
        self.assert_password_field_present()
        if type(username) is str:
            self.type_username(username)
            self.type_password('Tester#123')
            self.submit_to_create_a_student()
            self.assert_student_added_successfully()
        else:
            for i in range(0, len(username)):
                self.type_username(username[i])
                self.type_password('Tester#123')
                self.submit_to_create_a_student()
                self.assert_student_added_successfully()
                time.sleep(1)
        self.assert_close_button_present()
        self.click_on_close_button()


class YouHaveCreatedNewClassForm(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        with allure.step("Wait `Success Checkmark` to be located"):
            self.wait_until_element_located((By.XPATH,
                                             "//*[contains(@class,'loading-checkmark') and contains(@class,'is-active')]"))

    @allure.step("Verify the `Add Students` button of 'You`ve Created A New Class' form present")
    def assert_add_students_button_present(self):
        assert self.is_element_present(YouHaveCreatedNewClassLocator.add_students_button), \
            "The `Add Students` button of `You've` Created A new Class` form is missing"

    @allure.step("Verify the `Close` button of 'You`ve Created A New Class' form present")
    def assert_close_button_present(self):
        assert self.is_element_present(YouHaveCreatedNewClassLocator.close_button), \
            "The `Close` button of `You've` Created A new Class` form is missing"

    @allure.step("Click on the `Add Students` button of `You've Created A New Class` form")
    def click_on_add_students_button(self) -> AddStudentsForm:
        self.click_on_element(YouHaveCreatedNewClassLocator.add_students_button)
        return AddStudentsForm(self.driver)

    @allure.step("Click on the `Close` button of `You've Created A New Class` form")
    def click_on_close_button(self):
        self.click_on_element(YouHaveCreatedNewClassLocator.close_button)


class CreateAClassForm(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        with allure.step("Wait `Create A New Class` form to be located."):
            self.wait_until_element_located((By.XPATH,
                                             "//h3[contains(text(),'Add a Class')]"))
        time.sleep(0.5)

    @allure.step("Verify the `Class Name` field of `Create A New Class` form present")
    def assert_class_name_field_present(self):
        assert self.is_element_present(CreateAClassLocator.class_name_field), \
            'The `Class Name` field is missing from the `Create A New Class` form'

    @allure.step("Verify the `Create Class` button of `Create A New Class` form present")
    def assert_create_class_button_present(self):
        assert self.is_element_present(CreateAClassLocator.create_class_button), \
            'The `Create Class` button is missing from the `Create A New Class` form'

    @allure.step("Write `{1}` class name into the `Class Name` field of `Create A New Class` form")
    def type_class_name(self, class_name: str):
        self.find_element(CreateAClassLocator.class_name_field).send_keys(class_name)

    @allure.step("Submit to create class")
    def submit_to_create_class(self) -> YouHaveCreatedNewClassForm:
        self.find_element(CreateAClassLocator.class_name_field).submit()
        return YouHaveCreatedNewClassForm(self.driver)


class TeacherClassesPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.page = 'teacher/classes'
        with allure.step("Wait until `Teacher Classes` page to be loaded"):
            self.wait_until_element_located(TeacherClassesPageLocator.create_a_new_class_button)

    @allure.step("Verify the `Create A New Class` button of `Teacher Classes` page present")
    def assert_create_a_new_class_button_present(self):
        assert self.is_element_present(TeacherClassesPageLocator.create_a_new_class_button), \
            "The `Create A New Class` button is missing from the `Teacher Classes` page"

    @allure.step("Click on the `Create A New Class` button")
    def click_on_create_a_new_class_button(self):
        self.click_on_element(TeacherClassesPageLocator.create_a_new_class_button)
        return CreateAClassForm(self.driver)

    @allure.step("Verify the `First Class` present on `Teacher Classes` page.")
    def assert_first_class_present(self):
        assert self.is_element_present(TeacherClassesPageLocator.first_class), \
            "first class is missing"

    @allure.step("Verify first class title is `{1}`")
    def assert_first_class_title(self, exp):
        title = self.find_element(TeacherClassesPageLocator.first_class).find_element(
            *TeacherClassesPageLocator.class_title).text
        assert title == exp, \
            f"Expected class title to be `{exp}`, but was `{title}`"

    @allure.step("Verify first class students count is `{1}`")
    def assert_first_class_students_count(self, exp):
        title = self.find_element(TeacherClassesPageLocator.first_class).find_element(
            *TeacherClassesPageLocator.class_students_count).text.strip()
        assert title == str(exp), \
            f"Expected students count to be `{exp}`, but was `{title}`"

    @allure.step("Click on `{1}` class")
    def click_on_class(self, class_name):
        by, selector = TeacherClassesPageLocator.class_with_name[0], TeacherClassesPageLocator.class_with_name[
            1].replace('class_name', class_name)
        self.click_on_element((by, selector))
        return SingleClassPage(self.driver)


class CreateAssignmentForm(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step("Verify the `Create Assignment` button is present")
    def assert_create_assignment_button_present(self):
        assert self.is_element_present(CreateAssignmentLocator.create_assignment_button), \
            "The `Create Assignment` button is missing from the `Create Assignment` form"

    @allure.step("Verify the `Typing Lesson` is present")
    def assert_typing_lesson_present(self):
        assert self.is_element_present(CreateAssignmentLocator.typing_lesson), \
            "The `Typing Lesson` is missing from the `Create Assignment` form"

    @allure.step("Verify the `Digital Literacy Lesson` is present")
    def assert_digital_literacy_lesson_present(self):
        assert self.is_element_present(CreateAssignmentLocator.digital_literacy_lessons), \
            "The `Digital Literacy Lesson` is missing from the `Create Assignment` form"

    @allure.step("Verify the `Written Prompt` is present")
    def assert_written_prompt_present(self):
        assert self.is_element_present(CreateAssignmentLocator.written_prompt), \
            "The `Written Prompt` is missing from the `Create Assignment` form"

    @allure.step("Verify the `Typing Assignments` is present")
    def assert_typing_assessments_present(self):
        assert self.is_element_present(CreateAssignmentLocator.typing_assessments), \
            "The `Typing Assignments` is missing from the `Create Assignment` form"

    @allure.step("Verify the `Title` field is present")
    def assert_title_field_present(self):
        assert self.is_element_present(CreateAssignmentLocator.title_field), \
            "The `Title` field is missing from the `Create Assignment` form"

    @allure.step("Verify the `Prompt` field is present")
    def assert_prompt_field(self):
        assert self.is_element_present(CreateAssignmentLocator.prompt_field), \
            "The `Prompt` field is missing from the `Create Assignment` form"

    @allure.step("Verify the `Word Count` field is present")
    def assert_word_count_field(self):
        assert self.is_element_present(CreateAssignmentLocator.word_count), \
            "The `Word Count` field is missing from the `Create Assignment` form"

    @allure.step("Verify the `Select Lessons` dropdown is present")
    def assert_select_lessons_dropdown(self):
        assert self.is_element_present(CreateAssignmentLocator.select_lessons_dropdown), \
            "The `Select Lessons` dropdown is missing from the `Create Assignment` form"

    @allure.step("Verify the `Assignee To` dropdown is present")
    def assert_assignee_to_dropdown(self):
        assert self.is_element_present(CreateAssignmentLocator.assignee_to), \
            "The `Assignee To` dropdown is missing from the `Create Assignment` form"

    @allure.step("Verify the `Select Students` dropdown is present")
    def assert_select_students_dropdown(self):
        assert self.is_element_present(CreateAssignmentLocator.select_students), \
            "The `Select Students` dropdown is missing from the `Create Assignment` form"

    @allure.step("Click on `Typing Lesson`")
    def click_on_typing_lesson(self):
        self.click_on_element(CreateAssignmentLocator.typing_lesson)
        self.wait_title_field_to_be_visible()

    @allure.step("Click on `Digital Literacy Lesson`")
    def click_on_digital_literacy_lessons(self):
        self.click_on_element(CreateAssignmentLocator.digital_literacy_lessons)
        self.wait_title_field_to_be_visible()

    @allure.step("Click on `Typing Assignments`")
    def click_on_typing_assessments(self):
        self.click_on_element(CreateAssignmentLocator.typing_assessments)
        self.wait_title_field_to_be_visible()

    @allure.step("Click on `Written Prompt`")
    def click_on_written_prompt(self):
        self.click_on_element(CreateAssignmentLocator.written_prompt)
        self.wait_title_field_to_be_visible()

    def wait_title_field_to_be_visible(self):
        self.wait_until_element_located(CreateAssignmentLocator.title_field)

    @allure.step("Type {1} title into the `Title` field")
    def type_title_field(self, title):
        self.find_element(CreateAssignmentLocator.title_field).send_keys(title)

    @allure.step("Type {1} description into the `Prompt` field")
    def type_prompt_field(self, prompt):
        self.find_element(CreateAssignmentLocator.prompt_field).send_keys(prompt)

    @allure.step("Type {1} word count into the `Word Count` field")
    def type_word_count_field(self, word_count):
        self.find_element(CreateAssignmentLocator.word_count).send_keys(word_count)

    @allure.step("Select {1} from the `Select Lessons Dropdown` field")
    def select_from_select_lessons_dropdown(self, lessons):
        element = self.find_element(CreateAssignmentLocator.select_lessons_dropdown)
        element.send_keys(lessons)
        time.sleep(0.3)
        if os.environ['BROWSER'] == 'safari':
            element.send_keys(Keys.ENTER)
        else:
            self.click_on_element((By.XPATH, f"//ul[@class='chosen-results']/li[contains(text(),'{lessons}')]"))

    @allure.step("Select {1} from the `Assignee To Dropdown` field")
    def select_from_assignee_to_dropdown(self, class_name):
        self.click_on_element(CreateAssignmentLocator.assignee_to)
        time.sleep(0.3)
        self.click_on_element((By.XPATH, f"//ul[@class='chosen-results']/li[contains(text(),'{class_name}')]"))

    @allure.step("Select {1} from the `Select Students Dropdown` field")
    def select_from_select_students_dropdown(self, student_name):
        if type(student_name) is tuple:
            for i in range(0, len(student_name)):
                self.click_on_element(CreateAssignmentLocator.select_students)
                time.sleep(0.3)
                self.click_on_element(
                    (By.XPATH, f"//ul[@class='chosen-results']/li[contains(text(),'{student_name[i]}')]"))
                time.sleep(0.3)
        else:
            self.click_on_element(CreateAssignmentLocator.select_students)
            time.sleep(0.3)
            self.click_on_element((By.XPATH, f"//ul[@class='chosen-results']/li[contains(text(),'{student_name}')]"))

    @allure.step("Submit to create assignment")
    def submit_to_create_assignment(self):
        self.find_element(CreateAssignmentLocator.title_field).submit()

    def create_typing_lessons_assignment(self, title="Test", lessons="Skill Builder", classes=None, students=None):
        with allure.step(f"Create `Typing Lessons` assignment with `{title}` title and `{lessons}` lesson"):
            self.assert_typing_lesson_present()
            self.click_on_typing_lesson()
            time.sleep(0.5)
            self.assert_title_field_present()
            self.assert_select_lessons_dropdown()
            self.assert_create_assignment_button_present()
            self.assert_assignee_to_dropdown()
            self.assert_select_students_dropdown()
            if classes is not None:
                self.select_from_assignee_to_dropdown(classes)
            if students is not None:
                self.select_from_select_students_dropdown(students)
            self.type_title_field(title)
            self.select_from_select_lessons_dropdown(lessons)
            self.submit_to_create_assignment()
            self.wait_until_assignment_added_successfully()

    def create_digital_literacy_lessons_assignment(self, title="Test", lessons="Skill Builder"):
        with allure.step(f"Create `Digital Literacy Lessons` assignment with `{title}` title and `{lessons}` lesson"):
            self.assert_digital_literacy_lesson_present()
            self.click_on_digital_literacy_lessons()
            time.sleep(0.5)
            self.assert_title_field_present()
            self.assert_select_lessons_dropdown()
            self.assert_create_assignment_button_present()
            self.type_title_field(title)
            self.select_from_select_lessons_dropdown(lessons)
            self.submit_to_create_assignment()
            self.wait_until_assignment_added_successfully()

    def create_typing_assessment_assignment(self, title="Test", lessons="Skill Builder", classes=None, students=None):
        with allure.step(f"Create `Typing Assessment` assignment with `{title}` title and `{lessons}` lesson"):
            self.assert_typing_assessments_present()
            self.click_on_typing_assessments()
            time.sleep(0.5)
            self.assert_title_field_present()
            self.assert_select_lessons_dropdown()
            self.assert_create_assignment_button_present()
            self.assert_assignee_to_dropdown()
            self.assert_select_students_dropdown()
            if classes is not None:
                self.select_from_assignee_to_dropdown(classes)
            if students is not None:
                self.select_from_select_students_dropdown(students)
            self.type_title_field(title)
            self.select_from_select_lessons_dropdown(lessons)
            self.submit_to_create_assignment()
            self.wait_until_assignment_added_successfully()

    def create_written_prompt_assignment(self, title="Test", prompt="Test Prompt", word_count=9):
        with allure.step(
                f"Create `Typing Assessment` assignment with `{title}` title,`{prompt}` prompt and `{word_count}` Word count"):
            self.assert_written_prompt_present()
            self.click_on_written_prompt()
            time.sleep(0.5)
            self.assert_title_field_present()
            self.assert_prompt_field()
            self.assert_word_count_field()
            self.assert_create_assignment_button_present()
            self.type_title_field(title)
            self.type_prompt_field(prompt)
            self.type_word_count_field(word_count)
            self.submit_to_create_assignment()
            self.wait_until_assignment_added_successfully()

    # fixed z-50 notice bottom-4 right-4 notice-container js-notice notice--success
    @allure.step("Wait for success checkbox to be located")
    def wait_until_assignment_added_successfully(self):
        try:
            self.wait_until_element_located((By.XPATH, '//div[contains(@class, "notice--success")]'))
        except TimeoutException:
            assert False, \
                "The assignment doesn't created successfuly, Success checkbox missing"


class SingleClassPage(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        with allure.step("Wait until `Teacher Single Class` page to be loaded"):
            self.wait_until_element_is_invisible((By.CLASS_NAME, 'js-loading-animation'))
            self.wait_until_element_located((By.XPATH, "//h1[contains(@class,'leading-tight')]"))

    def refresh_page(self):
        super().refresh_page()
        return SingleClassPage(self.driver)

    @allure.step("Verify the `My Classes` link present")
    def assert_my_classes_link_present(self):
        assert self.is_element_present(SingleClassPageLocator.my_classes_link), \
            "The `My Classes` link is missing from the `Teacher Single Class` page"
        return self

    @allure.step("Verify the `Add Students` button present")
    def assert_add_students_button_present(self):
        assert self.is_element_present(SingleClassPageLocator.add_students_button), \
            "The `Add Students` button is missing from the `Teacher Single Class` page"
        return self

    @allure.step("Verify the `Students` tab present")
    def assert_students_tab_present(self):
        assert self.is_element_present(SingleClassPageLocator.students_tab), \
            "The `Students` tab is missing from the `Teacher Single Class` page"
        return self

    @allure.step("Verify students count is {1}")
    def assert_students_count_is(self, count):
        cnt = self.find_element(SingleClassPageLocator.students_tab).text.replace(" ", "")
        cnt = re.sub(r'\n\s\t', '', cnt)
        assert f'Students' in cnt and f"({count})" in cnt, \
            f"The expected value for `Students` tab is `Students({count})` but was `{cnt}`"
        return self

    @allure.step("Click on `Add Students` button")
    def click_on_add_students_button(self) -> AddStudentsForm:
        self.click_on_element(SingleClassPageLocator.add_students_button)
        return AddStudentsForm(self.driver)

    @allure.step("Click on `My Classes` link")
    def click_on_my_classes_link(self) -> TeacherClassesPage:
        self.click_on_element(SingleClassPageLocator.my_classes_link)
        return TeacherClassesPage(self.driver)

    @allure.step("Verify student with {1} username present")
    def assert_student_with_username_present(self, username):
        time.sleep(0.5)
        assert self.is_element_present(SingleClassPageLocator.first_student) or self.find_element(
            SingleClassPageLocator.first_student).text.replace(" ", "") == username, \
            f"Student with '{username}' username is missing"

    @allure.step("Verify the `assignments` tab present")
    def assert_assignments_tab_present(self):
        assert self.is_element_present(SingleClassPageLocator.assignments_tab), \
            "The `Assignments` tab is missing"
        return self

    @allure.step("Verify assignments count is {1}")
    def assert_assignments_tab_count_is(self, count):
        cnt = self.find_element(SingleClassPageLocator.assignments_tab).text.replace(" ", "")
        assert str(count) in cnt and "Assignments" in cnt, \
            f"The expected value for `Assignments` tab is `Assignments({count})` but was `{cnt}`"
        return self

    @allure.step("Verify assignment with {1} name present")
    def assert_assignment_by_name_present(self, assignment_name):
        locator = SingleClassPageLocator.assignment_by_name
        assert self.is_element_present((locator[0], locator[1].replace('replacement', assignment_name))), \
            f"The assignment with {assignment_name} is missing"
        return self

    @allure.step("Click on the `Assignment` tab")
    def click_on_assignments_tab(self):
        self.click_on_element(SingleClassPageLocator.assignments_tab)
        self.wait_until_element_located(SingleClassPageLocator.add_assignment_button)
        return self

    @allure.step("Click on the `Add Assignment` button")
    def click_on_add_assignment_button(self) -> CreateAssignmentForm:
        self.click_on_element(SingleClassPageLocator.add_assignment_button)
        return CreateAssignmentForm(self.driver)


class SingleClassPageLocator:
    add_students_button = (By.XPATH, "//button[contains(@class,'js-add-students')]")
    add_assignment_button = (By.XPATH, "//button[contains(@class,'js-add-assignment')]")
    students_tab = (By.XPATH, "//div[contains(@data-id,'students')]")
    assignments_tab = (By.XPATH, "//div[contains(@data-id,'assignments')]")
    assignment_by_name = (By.XPATH,
                          "//div[contains(@class,'js-assignments-table')]//tbody/tr/td/div/div[contains(text(),'replacement')]/ancestor::tr[contains(@class, 'group')]")
    settings_tab = (By.XPATH, "//div[contains(@data-id,'settings')]")
    first_student = (By.XPATH, "//tr[contains(@data-tour,'click-first-student')][1]/td[@class='td'][1]")
    my_classes_link = (By.XPATH, "//a[contains(text(),'My Classes')]")


class CreateAssignmentLocator:
    typing_lesson = (By.XPATH, "//div[@data-id='typing_lessons']")
    digital_literacy_lessons = (By.XPATH, "//div[@data-id='digital_literacy_lessons']")
    typing_assessments = (By.XPATH, "//div[@data-id='typing_assessments']")
    written_prompt = (By.XPATH, "//div[@data-id='written_prompt']")
    create_assignment_button = (By.XPATH, "//button[contains(text(), 'Create Assignment')]")
    title_field = (By.ID, "form-ele-title")
    select_lessons_dropdown = (By.XPATH, "//div[@id='form_ele_lesson_ids_chosen']//input")
    assignee_to = (By.ID, "form_ele_section_ids_chosen")
    select_students = (By.ID, "form_ele_user_ids_chosen")
    prompt_field = (By.XPATH, "//label[contains(text(),'Prompt')]/following-sibling::textarea")
    word_count = (By.ID, "form-ele-word_count")
    # select_lessons_dropdown = (By.ID, "")


class TeacherClassesPageLocator:
    create_a_new_class_button = (By.XPATH, "//button[@data-tour='click-add-class']")
    first_class = (By.XPATH, "//tr[@data-tour='first-class-row'][1]")
    class_with_name = (
        By.XPATH,
        "//tr[@data-tour='first-class-row']/td/div/div[contains(text(),'class_name')]/ancestor::tr[@data-tour='first-class-row']/td[2]")
    class_title = (By.XPATH, "//td[2]")
    class_students_count = (By.XPATH, "//td[3]")


class AddStudentsLocator:
    add_single_student_form = (By.XPATH, "//div[@data-id='addSingle']")
    create_single_student_button = (By.XPATH, "//button[contains(text(),'Create') and contains(text(),'Student')]")
    username_field = (By.ID, 'form-ele-username')
    password_field = (By.ID, 'form-ele-password')
    student_added_success = (By.XPATH, '//div[contains(@class, "notice--success")]')
    close_button = (By.XPATH, "//div[@data-el='modal-close']")


class YouHaveCreatedNewClassLocator:
    add_students_button = (By.XPATH, "//button[contains(@data-tour,'add-students')]")
    close_button = (By.XPATH, "//div[@data-el='modal-close']")


class CreateAClassLocator:
    class_name_field = (By.ID, "form-ele-name")
    create_class_button = (By.XPATH, "//button[contains(text(),'Create Class')]")
