from PIL import Image
from PIL import ImageChops

# https://stackoverflow.com/questions/35176639/compare-images-python-pil/56280735
production = Image.open("/Users/elenayanushevskaya/python_qa_screenshot/images/example_product.png").convert('RGB')
staging = Image.open("/Users/elenayanushevskaya/python_qa_screenshot/images/example_staging.png").convert('RGB')

# Find difference between images
difference = ImageChops.difference(production, staging)

if difference.getbbox():
    print("Different!")
    difference.save("/Users/elenayanushevskaya/python_qa_screenshot/images/example_compare_images_difference.png")
else:
    print("Not different!")
