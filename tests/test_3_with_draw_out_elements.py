import time
import allure
import pytest
from selenium.webdriver.common.by import By

from config import PROD_BASE_URL, STAGE_BASE_URL
from screenshots.helpers import comparison_test_light_with_draw, make_tmp_file_path


@allure.label("testType", "screenshotDiff")
@allure.title("Comparing pages test with draw elements out")
def test_main_page_draw_elements_out(browser):
    master_path = make_tmp_file_path(browser, "prod")
    staging_path = make_tmp_file_path(browser, "staging")
    diff_path = make_tmp_file_path(browser, "diff")

    browser.get(PROD_BASE_URL) # prod
    slider = browser.find_element(By.CSS_SELECTOR, '[data-ux="Block"]').rect
    browser.save_screenshot(master_path)

    browser.get(STAGE_BASE_URL) # stage
    browser.save_screenshot(staging_path)

    comparison_test_light_with_draw(
        master_path,
        staging_path,
        diff_path,
        draw_out=[slider],
        clear_images=False,
    )
