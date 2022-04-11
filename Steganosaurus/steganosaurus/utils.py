# utils.py
"""
Steganosaurus
    
Linden Crandall
Jonthan Mainhart
Zhihua Zheng

Final Project for CMSC 495.

April 11, 2022

Utility functions for Steganosaurus. 
"""

import PIL
import PySimpleGUI as dialog_pop_up
from PIL import Image
from tkinter.filedialog import askopenfilename

"""this image file utility is to be embedded into 
    a button component within 
    the main GUI application """

def open_image_file():
	"""	- opens file explorer on user's machine to select
		  image to be encoded

		- throws an error which is a dialog box
		  letting the user know that the file chosen
          is of an invalid format

		- takes no input"""
	
	try:
		# opens user's file explorer
		im = Image.open(askopenfilename())
	
		# This method will show image in any image viewer
		im.show()
	except IOError:
		
        # 
		dialog_pop_up.popup_ok("Oh no!",
		                          "You have to select an image file!\n"
		                          "Make sure the file you choose ends with "
		                          "one of these image extensions:\n"
		                          ".png, .jpg, .JPEG, .svg, .webp", )

# call the function 
open_image_file()
