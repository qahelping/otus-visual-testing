import time

import allure
import pytest
from selenium.webdriver.common.by import By

from config import PROD_BASE_URL, STAGE_BASE_URL
from screenshots.helpers import comparison_test_light, make_tmp_file_path


@allure.label("testType", "screenshotDiff")
@allure.title("Comparing pages test with basic comparison and actions")
def test_interactive_element(browser):
    prod_screenshot_path = '/Users/elenayanushevskaya/Desktop/QAP/otus-visual-testing/test_screenshots/test_interactive_element/28e2c_staging.png'
    # prod_screenshot_path = make_tmp_file_path(browser, "prod")
    stag_screenshot_path = make_tmp_file_path(browser, "staging")
    diff_screenshot_path = make_tmp_file_path(browser, "diff")

    for url, scr in [
        # (PROD_BASE_URL, prod_screenshot_path),
        (STAGE_BASE_URL, stag_screenshot_path),
    ]:
        browser.get(url)
        time.sleep(2)
        # browser.find_element(by=By.XPATH, value='//*[@id="popup-widget62629"]/div/div/div[1]').click()
        browser.save_screenshot(scr)

    comparison_test_light(
        prod_screenshot_path, stag_screenshot_path, diff_screenshot_path
    )
