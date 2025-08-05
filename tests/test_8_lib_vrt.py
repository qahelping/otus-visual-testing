from visual_regression_tracker import VisualRegressionTracker, Config, TestRun

config = Config(
    apiUrl='http://localhost:4200',
    project='bb840b96-6c6f-4ed8-979b-e0bbfa3fdc3f',
    apiKey='DEFAULTUSERAPIKEYTOBECHANGED',
    ciBuildId='commit_sha',
    branchName='develop',
    enableSoftAssert=False,
)


def test_visual_regression_tracker(browser):
    vrt = VisualRegressionTracker(config)

    with vrt:
        try:
            browser.get("https://candymapper.com/")
            browser.set_window_size(width=800, height=600)
            vrt.track(TestRun(
                name='psf-landing',
                imageBase64=browser.get_screenshot_as_base64(),
                diffTollerancePercent=0,
                os='Mac',
                browser='Chrome',
                viewport='800x600',
                device='PC',
            ))
        finally:
            browser.quit()


def test_visual_regression_tracker__diff_70(browser):
    vrt = VisualRegressionTracker(config)

    with vrt:
        try:
            browser.get("https://candymapper.com/")
            # browser.get("https://candymapperr2.com")
            browser.set_window_size(width=800, height=600)
            vrt.track(TestRun(
                name='python',
                imageBase64=browser.get_screenshot_as_base64(),
                diffTollerancePercent=70,
                os='Mac',
                browser='Chrome',
                viewport='800x600',
                device='PC',
            ))
        finally:
            pass
