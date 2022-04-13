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
import stego



def main():
    # open the GUI, after closing, rest of code below will execute, then gui window will close
    stego.MainFrame()
    

if __name__ == "__main__":
    main()
