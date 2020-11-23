import allure
import pytest
import os
import browsers
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


@pytest.fixture(scope="class")
def get_driver(request):
    browser = os.environ["BROWSER"]
    if browser == browsers.CHROME:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        if 'THROUGHPUT' in os.environ.copy():
            driver.set_network_conditions(
                offline=False,
                latency=5,
                throughput=int(os.environ['THROUGHPUT']) * 1024,
            )
    elif browser == browsers.FIREFOX:
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser == browsers.IE:
        driver = webdriver.Ie(IEDriverManager().install())
    elif browser == browsers.EDGE:
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    elif browser == browsers.SAFARI:
        driver = webdriver.Safari()

    driver.maximize_window()

    request.cls.driver = driver
    yield
    driver.close()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            allure.attach(item.instance.driver.get_screenshot_as_png(),
                          name=item.name,
                          attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print(e)
