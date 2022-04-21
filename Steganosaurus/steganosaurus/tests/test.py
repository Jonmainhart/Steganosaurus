# test.py
"""
Steganosaurus
    
Linden Crandall
Jonthan Mainhart
Zhihua Zheng

Final Project for CMSC 495.

April 19, 2022

Unit tests for Stenganosaurus application.
"""
import pytest
from os import path, remove
from models import ImageObject
from utils import convert_message

class TestImageObjectModel:
    """
    Test class for ImageObject methods.
    """
    # class constants for testing
    DEFAULT_MSG = 'the quick brown fox jumps over the lazy dog'
    IMG_TEST_IO = ImageObject(filename=path.abspath(path.join(path.dirname(__file__), 'test_image_0.jpeg')))
    IMG_5_PIX = ImageObject(filename=path.abspath(path.join(path.dirname(__file__), 'test_image_1.jpeg')))
    IMG_300_PIX = ImageObject(filename=path.abspath(path.join(path.dirname(__file__), 'test_image_2.jpeg')))
    # default save location is tests folder
    SAVE_PATH = path.abspath(path.join(path.dirname(__file__), ''))
    SAVE_NAME = 'test_save_image.png'


    def test_max_char_90000_pix(self):
        """
        Check the max_available_chars attribute of a known input
        """
        # 300 x 300 pixel image will be 30,000 chars
        # [(300 x 300 pix) * 3 color values per pixel] / (8 bits per char + 1 control bit) 
        assert self.IMG_300_PIX.max_available_chars == 30000

    def test_max_char_25_pix(self):
        """
        Check the max_available_chars attribute of a known input
        """
        # 5 x 5 pixel image will result in 8 chars using same formula
        assert self.IMG_5_PIX.max_available_chars == 8

    def test_max_char_limit(self):
        """
        Check the encode function does not truncate messages with
        length that is equal to max_available_chars attribute
        """
        # string length is max chars - will not truncate
        msg = '01234567'
        self.IMG_5_PIX.encode_image(msg)
        assert self.IMG_5_PIX.decode_image() == msg

    def test_max_char_overflow(self):
        """
        Check the encode function truncates messages with 
        length greater than max_available_chars attribute
        """
        # string will truncate - too long
        msg = '01234567ABCDEF'
        self.IMG_5_PIX.encode_image(msg)
        assert (self.IMG_5_PIX.decode_image() != msg and self.IMG_5_PIX.decode_image() == '01234567')

    def test_image_attribute_match(self):
        """
        Checks that backup attributes are exact copies
        """
        assert list(self.IMG_300_PIX._image.getdata()) == list(self.IMG_300_PIX._backup_image.getdata())

    def test_encode_image(self):
        """
        Checks _image attribute pixels are different than 
        _backup_image pixels after encoding
        """
        self.IMG_300_PIX.encode_image(self.DEFAULT_MSG)
        assert list(self.IMG_300_PIX._image.getdata()) != list(self.IMG_300_PIX._backup_image.getdata())

    def test_decode_image(self):
        """
        Checks that the message encoded during encode_test 
        is the same value as the input string
        """
        assert self.IMG_300_PIX.decode_image() == self.DEFAULT_MSG

    def test_save_image(self):
        """
        Checks the save_image() method saves the file in the correct location.
        """
        self.IMG_TEST_IO.encode_image(self.DEFAULT_MSG)
        self.IMG_TEST_IO.save_image(self.SAVE_PATH, self.SAVE_NAME)
        assert path.exists(path.abspath(path.join(path.dirname(__file__), f'{self.SAVE_PATH}/{self.SAVE_NAME}')))

    def test_saved_image_decode(self):
        """
        Checks that a saved image contains the same 
        encoded message as the parent image
        """
        saved_img = ImageObject(filename=path.abspath(path.join(path.dirname(__file__), f'{self.SAVE_PATH}/{self.SAVE_NAME}')))
        assert saved_img.decode_image() == self.IMG_TEST_IO.decode_image()
        # remove the saved_file from the disk
        try:
            remove(saved_img.filename)
        except FileNotFoundError: # this may occur on windows if os.path didn't do its job
            assert False
        except IsADirectoryError: # this shouldn't ever occur
            assert False # fail gracefully if it does

    def test_reset_image(self):
        """
        Checks the reset() method resets the pixel values of the image objects
        """
        # ensure images are encoded 
        self.IMG_300_PIX.encode_image(self.DEFAULT_MSG)
        self.IMG_5_PIX.encode_image(self.DEFAULT_MSG)
        self.IMG_TEST_IO.encode_image(self.DEFAULT_MSG)
        
        # reset encoded images to their original values
        self.IMG_300_PIX.reset_image()
        self.IMG_5_PIX.reset_image()
        self.IMG_TEST_IO.reset_image()
        
        # Test
        assert list(self.IMG_300_PIX._image.getdata()) == list(self.IMG_300_PIX._backup_image.getdata())
        assert list(self.IMG_5_PIX._image.getdata()) == list(self.IMG_5_PIX._backup_image.getdata())
        assert list(self.IMG_TEST_IO._image.getdata()) == list(self.IMG_TEST_IO._backup_image.getdata())

class TestUtilities:

    DEFAULT_MSG = 'the quick brown fox jumps over the lazy dog'

    def test_convert_message(self):

        test_list = []
        
        for i in self.DEFAULT_MSG:
            # create a binary list representing the test message
            test_list.append(format(ord(i), '08b'))
        
        # use the utility to convert the message
        bin_list = convert_message(self.DEFAULT_MSG)
        
        # assert they are the same
        assert bin_list == test_list

class TestFileIO:

    def test_file_input_exception(self):
        """
        design this to test to check that non-image files throw an exception
        and image files do not throw an exception
        """
        pass

    def test_file_output_exception(self):
        """
        design this to check exceptions thrown from save()
        """
        pass
