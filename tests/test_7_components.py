import time

import allure
import pytest
from selenium.webdriver.common.by import By

from screenshots.helpers import make_tmp_file_path, comparison_test_light


@allure.label("testType", "screenshotDiff")
@allure.title("Comparing elements of the page: {locator}")
@pytest.mark.only
def test_main_page_elements(browser):
    master_path = make_tmp_file_path(browser, "prod")
    staging_path = make_tmp_file_path(browser, "staging")
    difference = make_tmp_file_path(browser, "diff")
    browser.get('https://global.wildberries.ru/')
    time.sleep(3)
    browser.find_element(By.CSS_SELECTOR, '[class="header j-header header--sticky"]').screenshot(master_path)

    browser.get('https://www.wildberries.by/')
    time.sleep(3)
    browser.find_element(By.CSS_SELECTOR, '[class="header j-header"]').screenshot(staging_path)

    comparison_test_light(master_path, staging_path, difference, clear_images=False)
