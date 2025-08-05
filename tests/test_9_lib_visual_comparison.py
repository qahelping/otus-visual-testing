import time

import pytest
from selenium.webdriver.common.by import By
from visual_comparison.utils import ImageComparisonUtil

from config import PROD_BASE_URL, STAGE_BASE_URL
from screenshots.helpers import make_tmp_file_path


@pytest.mark.only
def test_visual_comparison(browser):
    master_path = make_tmp_file_path(browser, "prod")
    staging_path = make_tmp_file_path(browser, "staging")
    diff_path = make_tmp_file_path(browser, "diff")

    browser.get(PROD_BASE_URL)
    time.sleep(1)
    browser.save_screenshot(master_path)

    browser.get(STAGE_BASE_URL)
    time.sleep(1)
    browser.save_screenshot(staging_path)

    expected_image = ImageComparisonUtil.read_image(master_path)
    actual_image = ImageComparisonUtil.read_image(staging_path)

    similarity_index = ImageComparisonUtil.compare_images(expected_image, actual_image, diff_path)
    print("Similarity Index:", similarity_index)

    match_result = ImageComparisonUtil.check_match(master_path, staging_path)
    assert match_result

@pytest.mark.only
def test_visual_comparison_element(browser):
    master_path = make_tmp_file_path(browser, "prod")
    staging_path = make_tmp_file_path(browser, "staging")
    diff_path = make_tmp_file_path(browser, "diff")

    browser.get('https://global.wildberries.ru/')
    time.sleep(3)
    browser.find_element(By.CSS_SELECTOR, '[class="header j-header header--sticky"]').screenshot(master_path)

    browser.get('https://www.wildberries.by/')
    time.sleep(3)
    browser.find_element(By.CSS_SELECTOR, '[class="header j-header"]').screenshot(staging_path)


    expected_image = ImageComparisonUtil.read_image(master_path)
    actual_image = ImageComparisonUtil.read_image(staging_path)

    similarity_index = ImageComparisonUtil.compare_images(expected_image, actual_image, diff_path)
    print("Similarity Index:", similarity_index)

    match_result = ImageComparisonUtil.check_match(master_path, staging_path)
    assert match_result