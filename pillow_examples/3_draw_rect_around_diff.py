from PIL import Image, ImageDraw

FACTOR = 1000
COLS = 90
ROWS = 80


def region_analyze(image, x, y, width, height, factor=FACTOR):
    region_status = 0

    for x_cord in range(x, x + width):
        for y_cord in range(y, y + height):
            try:
                pixel = image.getpixel((x_cord, y_cord))
                region_status += int(sum(pixel) / 3)
            except:
                return None
    return region_status // factor


def analyze(image_production, image_staging, col=COLS, row=ROWS):
    production = Image.open(image_production)
    staging = Image.open(image_staging)

    width, height = production.size
    block_width = width // col
    block_height = height // row

    has_diff = False

    for x in range(0, width, block_width + 1):
        for y in range(0, height, block_height + 1):

            region_ref = region_analyze(production, x, y, block_width, block_height)
            region_target = region_analyze(staging, x, y, block_width, block_height)

            if region_ref and region_target and region_ref != region_target:
                has_diff = True
                draw = ImageDraw.Draw(production)
                draw.rectangle(
                    (x - 1, y - 1, x + block_width, y + block_height),
                    outline="red",
                    width=2
                )


    if has_diff:
        production.save("/Users/elenayanushevskaya/QAP/otus-visual-testing/images/example_product_diff.png")
        print("Images are not identical")
    else:
        print("Images are identical on: FACTOR {f}, COLS {c}, ROWS {r}".format(f=FACTOR, c=COLS, r=ROWS))


if __name__ == "__main__":
    analyze(
        "/Users/elenayanushevskaya/QAP/otus-visual-testing/images/example_product.png",
        "/Users/elenayanushevskaya/QAP/otus-visual-testing/images/example_staging.png"
    )
