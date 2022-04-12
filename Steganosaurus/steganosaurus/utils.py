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
import sys
# image file chooser imports using ktinker (I had to do it >_<)
import PySimpleGUI as dialog_pop_up
from PIL import Image
from tkinter.filedialog import askopenfilename

"""this image file utility is to be embedded into
    a button component within
    the main GUI application
"""
def open_image():
        """
        opens file explorer on user's machine to select
        image to be encoded
        throws an error which is a dialog box
        letting the user know that the file chosen
        is of an invalid format
        takes no input
        """
        
        try:
            # opens user's file explorer to get image
            # askopenfilename returns a string which is the file path
            # that we need for further processing
            image_path = askopenfilename()
            # attempts to set this file to an imagev file type, else throw exception
            im = Image.open(image_path)
            
            # This method will show image in any image viewer
            # don't need to use this if GUI is handling it
            # im.show()
            # image file path that is needed for further processing
            print(f"\n*** Image path: '{image_path}' ***\n")
            return image_path
        except IOError:
            
            # dialog popup if user selects a file that is not an image type
            # this will be erased and the exception will be thrown to a dedicated
            # error handler, just used for testing purposes
            dialog_pop_up.popup_ok("Oh no!",
                                "You have to select an image file!\n"
                                "Make sure the file you choose ends with "
                                "one of these image extensions:\n"
                                ".png, .jpg, .JPEG, .svg, .webp", )
        
        #if user exits out of explorer without selecting a file
        # this will be erased and the exception will be thrown to a dedicated
        # error handler, just used for testing purposes
        except AttributeError:
            # dialog popup
            dialog_pop_up.popup_ok("Oh no!",
                               "You have to select an image file!\n"
                            "Make sure the file you choose ends with "
                             "one of these image extensions:\n"
                             ".png, .jpg, .JPEG, .svg, .webp", )

# choosing random image either 0.jpg or 1.jpg
def random_img() -> str:
	"""
	Private function for use by open_image_file to open a random default image

	Returns:
		int: References image in assets folder.
	"""
	# os.path.dirname(__file__) returns the current directory where this python
	# program is located.
	assets_path = os.path.dirname(__file__)
	# path of current directory to load random image
	img: str = f'{assets_path}/assets/{random.randint(0, 1)}.jpeg' # change upper bound to match files in assets folder
	
	print("Image:" + img)
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


