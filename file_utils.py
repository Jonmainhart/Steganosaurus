import PIL
import PySimpleGUI as dialog_pop_up
from PIL import Image
from tkinter.filedialog import askopenfilename

"""this image file utility is to be embedded into 
    a button component within 
    the main GUI application """

def open_image_file():
	"""opens file exploer on user's machine to select
		image to be encoded
		throws an error which is a dialog box
		letting the user know that the file chosen
        is of an invalid format"""
	
	try:
		#image_file = askopenfilename()
		# PIL stuff
		# open method used to open different extension image file
		im = Image.open(askopenfilename())
		
		# loads pixel data that is needed to extract bits and encode/decode message
		PIL.Image.Image.load(im)
	
	
		# This method will show image in any image viewer
		im.show()
	except IOError:
		
        # 
		dialog_pop_up.popup_ok("Oh no!",
		                          "You have to select an image file!\n"
		                          "Make sure the file you choose ends with "
		                          "one of these image extensions:\n"
		                          ".png, .jpg, .JPEG, .svg, .webp", )

open_image_file()
