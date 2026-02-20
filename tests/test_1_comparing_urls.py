import time

import allure
import pytest

from config import PROD_BASE_URL, STAGE_BASE_URL
from screenshots.helpers import comparison_test_light, make_tmp_file_path


@allure.label("testType", "screenshotDiff")
@allure.title("Comparing pages test with basic comparison")
@pytest.mark.only
def test_main_page(browser):
    master_path = make_tmp_file_path(browser, "prod")
    staging_path = make_tmp_file_path(browser, "staging")
    diff_path = make_tmp_file_path(browser, "diff")

    browser.get(PROD_BASE_URL)
    time.sleep(1)
    browser.save_screenshot(master_path)

    browser.get(STAGE_BASE_URL)
    time.sleep(1)
    browser.save_screenshot(staging_path)

    comparison_test_light(master_path, staging_path, diff_path, clear_images=False)


@allure.label("testType", "screenshotDiff")
@allure.title("Comparing pages test with basic comparison")
@pytest.mark.only
def test_main_page2(browser):
    master_path = 'test_screenshots/test_main_page/1fa43_staging.png'
    staging_path = make_tmp_file_path(browser, "staging")
    diff_path = make_tmp_file_path(browser, "diff")

    browser.get(STAGE_BASE_URL)
    time.sleep(1)
    browser.save_screenshot(staging_path)

    comparison_test_light(master_path, staging_path, diff_path, clear_images=False)
