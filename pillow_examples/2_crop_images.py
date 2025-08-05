from PIL import Image

image = Image.open('/Users/elenayanushevskaya/python_qa_screenshot/images/example_product.pngexample_product.png')
cropped = image.crop((0, 100, 200, 400))

cropped.save('/Users/elenayanushevskaya/python_qa_screenshot/images/example_product_cropped.png')
