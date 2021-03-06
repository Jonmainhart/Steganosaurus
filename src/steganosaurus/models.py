# models.py
"""
Steganosaurus
    
Linden Crandall
Jonthan Mainhart
Zhihua Zheng

Final Project for CMSC 495.

April 11, 2022

Object models for Steganosaurus.
"""
from PIL import Image
from utils import random_img, convert_message


class ImageObject:

    def __init__(self, filename=random_img()): # default constructor selects random image from assets/    
        self.filename: str = filename
        self._backup_image = Image.open(self.filename, 'r') # private ImageCore Object
        self._image = self._backup_image.copy()
        self.max_available_chars: int = self._calculate_max_chars()
    
    def _calculate_max_chars(self) -> int: # returns an int to caller
        
        # counts each pixel - 300 x 300 pic returns 90,000 pix
        num_of_pixels = len(self._image.getdata()) 
        
        # pixels * 3 (red, green, blue) / 9 (8-bit char + 1 control bit)
        max_chr = int(((num_of_pixels * 3) / 9)) # cast to int - division returns float

        return max_chr

    def _modify_pixels(self, pix, data: list):
        # TODO - reduce complexity
        """
        Private.
        Modifies the RGB values of the pixels of the ImageCore object by shifting 
        the value of each pixel to be either odd for a binary 1 or even for a binary 0.
        Will truncate messages greater than max_available_chars

        Adapted from https://www.geeksforgeeks.org/image-based-steganography-using-python/

        Args:
            pix: Image data
            data (list): binary encoded characters

        Yields:
            _type_: tuple generator
        """
        data_length = len(data)
        image_data = iter(pix)

        # FIX ISSUE 9
        # Truncate messages greater than max_available_chars
        if data_length > self.max_available_chars:
            data = data[:self.max_available_chars]
            data_length = len(data)

        for i in range(data_length):

            # Extract 3 pixels at a time
            pixels = [value for value in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]

            # Pixel value will shift odd for 1 and even for 0
            for j in range(0, 8): # upper bound not included
                if (data[i][j] == '0' and pixels[j]% 2 != 0): # make even
                    pixels[j] -= 1

                elif (data[i][j] == '1' and pixels[j] % 2 == 0): # make odd
                    if(pixels[j] != 0):
                        pixels[j] -= 1
                    else:
                        pixels[j] += 1
            
            # The ninth pixel of every set determins whether to continue reading or to stop
            # 0 means keep reading; 1 means stop
            if (i == data_length - 1):
                if (pixels[-1] % 2 == 0):
                    if(pixels[-1] != 0):
                        pixels[-1] -= 1
                    else:
                        pixels[-1] += 1

            else:
                if (pixels[-1] % 2 != 0):
                    pixels[-1] -= 1

            pixels = tuple(pixels)
            yield pixels[0:3]
            yield pixels[3:6]
            yield pixels[6:9]
    
    def encode_image(self, user_input: str):
        """
        Encodes a user-generated message in the rgb pixel data of the image object.

        Adapted from https://www.geeksforgeeks.org/image-based-steganography-using-python/

        Args:
            user_input (str): User-generated string.
        """

        w = self._image.size[0]
        (x, y) = (0, 0)

        for pixel in self._modify_pixels(self._image.getdata(),convert_message(user_input)):
            self._image.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1
        
    def decode_image(self) -> str:
        """
        Decodes message hidden in pixel data of an image.

        Adapted from https://www.geeksforgeeks.org/image-based-steganography-using-python/

        Returns:
            str: hidden message
        """
        
        msg = ''
        image_data = iter(self._image.getdata())

        try:
            while(True): # TODO - refactor to eliminate while true
                pixels = [value for value in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]
                bin_str = ''

                for i in pixels[:8]:
                    if (i % 2 == 0):
                        bin_str += '0'
                    else:
                        bin_str += '1'
                
                msg += chr(int(bin_str, 2))
                if (pixels[-1] % 2 != 0):
                    return msg
        except StopIteration:
            # Hacky fix to catch the StopIteration issue that occurs with some images
            # that do not have anything encoded. 
            return ''

    def reset_image(self):
        """
        Resets image to original pixel values.
        """
        
        self._image = self._backup_image.copy()

    def save_image(self, filepath: str, filename: str):
        """
        Save the image to the chosen filepath/filename

        Args:
            filepath (str): path/to/directory
            filename (str): filename without extension
        """
        fp = filepath + '/' + filename
        self._image.save(fp, format='PNG', quality=100, subsampling=0)
