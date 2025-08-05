from PIL import Image, ImageDraw, ImageFont

image_object = Image.open("/Users/elenayanushevskaya/python_qa_screenshot/images/example_product.png").convert("RGB")

draw_object = ImageDraw.Draw(image_object)
text = "Эта надпись раньше тут не была"

# font = ImageFont.truetype("Roboto-Thin.ttf", size=60)
#
# draw_object.text((100, 100), text, font=font)
draw_object.rectangle((300, 300, 600, 600), fill="blue")

image_object.save('/Users/elenayanushevskaya/python_qa_screenshot/images/example_product_tag.png')
