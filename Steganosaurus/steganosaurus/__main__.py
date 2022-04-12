#! python3
# __main__.py
"""
Steganosaurus
    
Linden Crandall
Jonthan Mainhart
Zhihua Zheng

Final Project for CMSC 495.

April 11, 2022

Main file for Steganosaurus.

Steganosaurus is an image-based steganography application written in Python.
"""

from utils import open_image
from models import ImageObject



def main():
    img = ImageObject() # get image from assets folder in models.py ImageObject class
    print(f"Image file name: {img}\n")
    print('Image memory location')
    print(img.rgb_pixel_data)
    print(f'THIS IS THE MAX CHAR >>> {img._calculate_max_chars()}')
    print('Comparing original to backup...')
    print(list(img.rgb_pixel_data) == list(img._backup_pixel_data))
    print('encoding image with "hello" ... ')
    img.encode_image('hello')
    print('Comparing ,modified value with back up ... ')
    print(list(img.rgb_pixel_data) == list(img._backup_pixel_data))
    print(f'The hidden message is {img.decode_image()}')
    print('resetting original ... ')
    img.reset_image()
    print('comparing reset value with backup')
    print(list(img.rgb_pixel_data) == list(img._backup_pixel_data))
    print('get a new image')
    img = ImageObject(open_image())
    print(img.filename)
    print(type(img))
    print(type(img.rgb_pixel_data))
    print(type(img._image))


if __name__ == "__main__":
    main()
