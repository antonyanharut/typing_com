import allure
import requests
from random import randint

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver


@allure.step("Create a new teacher account using the APIs.")
def create_teacher_account():
    create_url = 'https://www.typing.com/apiv1/teacher/auth/signup'
    create_headers = {"content-type": "application/json"}
    email = f"test{randint(10, 99)}tester{randint(1000, 9999)}@yopmail.com"
    name = "Test Tester"
    password = "Tester123"
    crate_body = {"login_type": "username", "full_name": f"{name}", "email": f"{email}", "password": f"{password}"}
    create_teacher = requests.post(url=create_url, headers=create_headers, json=crate_body)
    token = create_teacher.json()['token']
    teacher_id = create_teacher.json()['teacher_id']
    requests.post(url='https://www.typing.com/apiv1/teacher/account/convert', headers={
        'content-type': 'application/json',
        'authorization': f'Bearer {token}'
    }, json={
        "district_name": "School N5",
        "school_name": "School N5",
        "license_type": "classroom",
        "org_type": "teacher",
        "other": "",
        "country": "AM",
        "name": "School N5",
        "tos": "1",
        "allow_contact": "1"
    })
    return {'email': email, 'password': password, 'name': name, 'teacher_id': teacher_id}


@allure.step("DELETE account using cache via APIs")
def delete_teacher_using_cache(driver: WebDriver):
    try:
        jwt_token = driver.execute_script("return window.localStorage.getItem('teacher_jwt_token')")
        print("test")
        print(type(jwt_token))
        login_data = login_with_token(jwt_token)
        with allure.step(f"DELETE `{login_data['email']}` account."):
            delete_teacher(login_data['teacher_id'], login_data['token'])
    except WebDriverException:
        pass


def login_with_token(token: str):
    url = 'https://www.typing.com/apiv1/teacher/auth/oauth-login'
    data = 'language=en'
    header = {'authorization': f'Bearer {token}'}
    login_date = requests.post(url=url, data=data, headers=header).json()
    return login_date


def delete_teacher(teacher_id: str, token: str):
    url = f'https://www.typing.com/apiv1/teacher/teachers/{teacher_id}'
    header = {'authorization': f'Bearer {token}'}
    result = requests.delete(url=url, headers=header)
    if result.text == '[]':
        with allure.step('Account DELETED successfully.'):
            pass


def create_student_account():
    url = 'https://www.typing.com/apiv1/student/auth/signup'
    username = f'tester{randint(10,99)}test{randint(1000,9999)}'
    password = 'Tester#123'
    body_json = {"username":f"{username}","password":f"{password}","password2":"","email":"","language":"","join_code":"","tos":"1"}
    response = requests.post(url=url, json=body_json).json()
    print(response)
    return {'username': response['username'], 'password': password }