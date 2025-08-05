import allure
import pytest

from config import PROD_BASE_URL, STAGE_BASE_URL
from screenshots.helpers import comparison_test_light, make_tmp_file_path


@allure.label("testType", "screenshotDiff")
@pytest.mark.parametrize("screen", ["640x700", "1024x768", "1920x1080"])
@allure.title("Comparing pages with rectangles: {screen}")
def test_main_page_scaling(browser, screen):
    browser.set_window_size(*screen.split("x"))
    master_path = make_tmp_file_path(browser, "prod")
    staging_path = make_tmp_file_path(browser, "staging")
    diff_path = make_tmp_file_path(browser, "diff")

    browser.get(PROD_BASE_URL)
    browser.save_screenshot(master_path)

    browser.get(STAGE_BASE_URL)
    browser.save_screenshot(staging_path)

    comparison_test_light(master_path, staging_path, diff_path, clear_images=False)
