from PIL import Image

image = Image.open('/Users/elenayanushevskaya/QAP/otus-visual-testing/images/example_product.png')
cropped = image.crop((0, 100, 200, 400))

cropped.save('/Users/elenayanushevskaya/QAP/otus-visual-testing/images/example_product_cropped.png')
