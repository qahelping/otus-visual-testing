import time
import allure
from selenium.webdriver.common.by import By

from config import PROD_BASE_URL, STAGE_BASE_URL
from screenshots.helpers import comparison_test_light, make_tmp_file_path


@allure.label("testType", "screenshotDiff")
@allure.title("Comparing pages test with basic")
def test_main_page_remove_elements(browser):
    master_path = make_tmp_file_path(browser, "prod")
    staging_path = make_tmp_file_path(browser, "staging")
    diff_path = make_tmp_file_path(browser, "diff")

    def remove_elements(driver, selectors: list):
        for selector in selectors:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            driver.execute_script("""
            var element = arguments[0];
            element.remove();;
            """, element)

    elements_prod = ['#popup-widget7437']
    elements_stage = ['#popup-widget62629']
    browser.get(PROD_BASE_URL)
    time.sleep(3)  # We want slider swipe
    remove_elements(browser, elements_prod)
    browser.save_screenshot(master_path)

    browser.get(STAGE_BASE_URL)
    remove_elements(browser, elements_stage)
    browser.save_screenshot(staging_path)

    comparison_test_light(master_path, staging_path, diff_path, clear_images=False)
