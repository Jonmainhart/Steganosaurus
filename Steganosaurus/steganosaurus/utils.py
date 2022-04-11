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

import random

##############################################
# CLEAN UP ANY UNUSED IMPORTS ON NEXT COMMIT #
##############################################

# import PIL
# import PySimpleGUI as dialog_pop_up
# from PIL import Image
# from tkinter.filedialog import askopenfilename

def random_img() -> str:
	"""
	Private function for use by open_image_file to open a random default image

	Returns:
		int: References image in assets folder.
	"""
	img: str = f'assets/{random.randint(0, 1)}.jpeg' # change upper bound to match files in assets folder
	
	return img

def convert_message(user_input: str) -> list:
	"""
	Converts a user-provided string into it's binary equivalent.

	Args:
		String (user_input): user-generated string

	Returns:
		list: The binary values of each character within the string.
	"""
	binlist = [0] # init with 0 so will not return a null if an empty string is passed

	if user_input is not None:
		binlist.pop() # remove the 0 before proceeding

	for i in user_input:
		binlist.append(format(ord(i), '08b'))
	
	return binlist


	
#######################################################################
# EVERYTHING BELOW THIS LINE IS OLD AND SHOULD PROBABLY BE RE-THUNK'D #
#######################################################################
"""this image file utility is to be embedded into 
    a button component within 
    the main GUI application 

def open_image_file():
		- opens file explorer on user's machine to select
		  image to be encoded

		- throws an error which is a dialog box
		  letting the user know that the file chosen
          is of an invalid format

		- takes no input
	
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
"""