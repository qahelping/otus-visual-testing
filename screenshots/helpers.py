import allure
import os

from io import BytesIO
from PIL import ImageChops
from PIL import Image, ImageDraw
from config import TMP_FOLDER


def make_tmp_file_path(browser, name):
    test_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    path = os.path.join("test_screenshots", f"{test_name}/{browser.session_id[:5]}_{name}.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path



def comparison_test_light(
    master_screenshot_path,
    staging_screenshot_path,
    difference_screenshot_path,
    clear_images=True
):
    """Simple image comparison function
    :param master_screenshot:
    :param staging_screenshot:
    :return:
    """
    master_screenshot = Image.open(master_screenshot_path).convert('RGB')
    staging_screenshot = Image.open(staging_screenshot_path).convert('RGB')

    # Returning the bbox diff for images
    result = ImageChops.difference(master_screenshot, staging_screenshot)

    try:
        assert not result.getbbox()
    except AssertionError:

        def buff(img):
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            return buffered.getvalue()

        result.save(difference_screenshot_path)

        allure.attach(
            name="expected",
            body=buff(master_screenshot),
            attachment_type=allure.attachment_type.PNG
        )

        allure.attach(
            name="actual",
            body=buff(staging_screenshot),
            attachment_type=allure.attachment_type.PNG
        )

        allure.attach(
            name="diff",
            body=buff(result),
            attachment_type=allure.attachment_type.PNG
        )

        msg = "Found difference: {} for master: {} vs. develop: {}"

        raise AssertionError(
            msg.format(
                result.getbbox(),
                master_screenshot_path,
                staging_screenshot_path
            )
        )
    finally:
        if clear_images:
            os.remove(master_screenshot_path)
            os.remove(staging_screenshot_path)
            if os.path.exists(difference_screenshot_path):
                os.remove(difference_screenshot_path)


def comparison_test_light_with_draw(
    master_screenshot_path,
    staging_screenshot_path,
    difference_screenshot_path,
    clear_images=True,
    draw_out=None
):
    """Besides comparison this function cad draw elements out
    :param master_screenshot:
    :param staging_screenshot:
    :return:
    """
    master_screenshot = Image.open(master_screenshot_path).convert("RGB")
    staging_screenshot = Image.open(staging_screenshot_path).convert("RGB")

    # Logic for drawing out the areas given to script
    if draw_out:
        for element in draw_out:
            draw_master = ImageDraw.Draw(master_screenshot)
            draw_staging = ImageDraw.Draw(staging_screenshot)

            dimensions = (
                int(element["x"]), int(element["y"]),
                int(element["x"]) + int(element["width"]),
                int(element["y"]) + int(element["height"]),
            )

            draw_master.rectangle(dimensions, fill="red")
            draw_staging.rectangle(dimensions, fill="red")

    # Returning the bbox diff for images
    result = ImageChops.difference(
        master_screenshot,
        staging_screenshot
    )

    try:
        assert not result.getbbox()
    except AssertionError:

        def buff(img):
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            return buffered.getvalue()

        result.save(difference_screenshot_path)

        allure.attach(
            name="expected",
            body=buff(master_screenshot),
            attachment_type=allure.attachment_type.PNG
        )

        allure.attach(
            name="actual",
            body=buff(staging_screenshot),
            attachment_type=allure.attachment_type.PNG
        )

        allure.attach(
            name="diff",
            body=buff(result),
            attachment_type=allure.attachment_type.PNG
        )

        msg = "Found difference: {} for master: {} vs. develop: {}"

        raise AssertionError(
            msg.format(result.getbbox(), master_screenshot, staging_screenshot)
        )

    finally:
        pass
        # if clear_images:
        # os.remove(master_screenshot_path)
        # os.remove(staging_screenshot_path)
        # if os.path.exists(difference_screenshot_path):
        #     os.remove(difference_screenshot_path)


def compare_images_hard(master_screenshot, develop_screenshot, factor=1000, cols=90, rows=80, clear_image=True):
    def _region_analyze(image, x, y, width, height, factor):
        region_status = 0

        for x_cord in range(x, x + width):
            for y_cord in range(y, y + height):
                try:
                    pixel = image.getpixel((x_cord, y_cord))
                    region_status += int(sum(pixel) / 3)
                except:
                    return None
        return region_status // factor

    def analyze(image_production, image_staging, factor, col, row, clear_image=clear_image):
        production = Image.open(image_production)
        staging = Image.open(image_staging)

        width, height = production.size
        block_width = width // col
        block_height = height // row

        has_diff = False

        for x in range(0, width, block_width + 1):
            for y in range(0, height, block_height + 1):

                region_ref = _region_analyze(production, x, y, block_width, block_height, factor)
                region_target = _region_analyze(staging, x, y, block_width, block_height, factor)

                if region_ref and region_target and region_ref != region_target:
                    has_diff = True
                    draw = ImageDraw.Draw(staging)
                    draw.rectangle(
                        (x - 1, y - 1, x + block_width, y + block_height),
                        outline="red", width=1
                    )

        def buff(img):
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            return buffered.getvalue()

        if clear_image:
            os.remove(image_production)
            os.remove(image_staging)

        if has_diff:
            allure.attach(buff(production), attachment_type=allure.attachment_type.PNG, name='expected')
            allure.attach(buff(staging), attachment_type=allure.attachment_type.PNG, name='actual')
            raise AssertionError('Найдены различия при сравнении скриншотов')

    analyze(master_screenshot, develop_screenshot, factor, cols, rows)
