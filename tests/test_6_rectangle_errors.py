import allure

from config import PROD_BASE_URL, STAGE_BASE_URL
from screenshots.helpers import compare_images_hard, make_tmp_file_path


@allure.label("testType", "screenshotDiff")
@allure.title("Comparing pages test with rectangle diff")
def test_main_page_rectangles(browser):
    master_path = make_tmp_file_path(browser, "prod")
    staging_path = make_tmp_file_path(browser, "staging")
    diff_path = make_tmp_file_path(browser, "diff")

    browser.get(PROD_BASE_URL)
    browser.save_screenshot(master_path)

    browser.get(STAGE_BASE_URL)
    browser.save_screenshot(staging_path)

    compare_images_hard(master_path, staging_path, diff_path)
