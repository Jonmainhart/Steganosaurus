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
import os


# choosing random image either 0.jpg or 1.jpg
def random_img() -> str:
	"""
	Private function for use by open_image_file to open a random default image

	Returns:
		int: References image in assets folder.
	"""
	# returns the absolute path of the __file__ object
	# should work across all file systems
	assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/'))
	
	# path to load random image
	img: str = f'{assets_path}/{random.randint(0, 3)}.jpeg' # change upper bound to match files in assets folder
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


