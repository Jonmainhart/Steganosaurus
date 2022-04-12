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

import utils
from models import ImageObject



def main():
    img = ImageObject() # get image from assets folder in models.py ImageObject class
    print(f"Image file name: {img}\n")
    print('Image memory location')
    print(img.rgb_pixel_data)
    print('Comparing original to backup...')
    print(list(img.rgb_pixel_data) == list(img._backup_pixel_data))
    print('encoding image with "hello" ... ')
    img.encode_image('hello')
    print('Comparing ,modified value with back up ... ')
    print(list(img.rgb_pixel_data) == list(img._backup_pixel_data))
    print('resetting original ... ')
    img.reset_image()
    print('comparing reset value with backup')
    print(list(img.rgb_pixel_data) == list(img._backup_pixel_data))


if __name__ == "__main__":
    main()
