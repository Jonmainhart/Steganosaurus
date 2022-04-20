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
from os import path
from models import ImageObject
from utils import convert_message

class Model:

    def __init__(self):
        self.test_image = ImageObject(filename=path.abspath(path.join(path.dirname(__file__), '../../assets/300.jpeg')))
        self.test_message = 'the quick brown fox jumps over the lazy dog'
        

class TestModel:
    """
    Test class for ImageObject methods.
    """
    #TODO - refactor each assert into a separate test
    def test_max_char(self):
        img = Model()
        # 300 x 300 pixel image will be 30,000 chars
        # [(300 x 300 pix) * 3 color values per pixel] / (8 bits per char + 1 control bit) 
        assert img.test_image.max_available_chars == 30000

    def test_max_char_2(self):
        img = ImageObject(filename=path.abspath(path.join(path.dirname(__file__), '../../assets/test_image_1.jpeg')))
        # 5 x 5 pixel image will result in 8 chars
        assert img.max_available_chars == 8

    def test_max_char_overflow(self):
        img = ImageObject(filename=path.abspath(path.join(path.dirname(__file__), '../../assets/test_image_1.jpeg')))
        # string is max chars
        msg = '01234567'
        img.encode_image(msg)
        encoded_msg = img.decode_image()
        assert encoded_msg == msg

    def test_encode_image(self):
        img = Model()
        assert list(img.test_image._image.getdata()) == list(img.test_image._backup_image.getdata())
        img.test_image.encode_image(img.test_message)
        # check that the decoded image is the same as the test message
        assert img.test_image.decode_image() == img.test_message
        
        # check the image object does not match backup
        assert img.test_image._image.getdata() != img.test_image._backup_image.getdata()

    def test_decode_image(self):
        img = Model()
        message = img.test_image.decode_image()
        # check that the test image does not have the test message encoded
        assert message != img.test_message
        # encode the image with the test message
        img.test_image.encode_image(img.test_message)
        # check that the decoder produces the same test message
        assert img.test_image.decode_image() == img.test_message

    def test_reset_image(self):
        img = Model()
        original_message = img.test_image.decode_image()

        img.test_image.encode_image(img.test_message)
        
        assert img.test_image.decode_image() == img.test_message
        # reset the image
        img.test_image.reset_image()
        # check the decoded message does not equal the test message
        assert img.test_image.decode_image() != img.test_message
        # check the decoded message matches the original
        assert img.test_image.decode_image() == original_message

    def test_save_image(self):
        img = ImageObject(filename=path.abspath(path.join(path.dirname(__file__), '../../assets/test_image_0.jpeg')))
        test_message = 'the quick brown fox jumps over the lazy dog'
        save_path = path.abspath(path.join(path.dirname(__file__), '../../assets'))
        save_name = 'test_save_image.png'
        img.encode_image(test_message)
        img.save_image(save_path, save_name)
        saved_img = ImageObject(filename=path.abspath(path.join(path.dirname(__file__), f'{save_path}/{save_name}')))
        decoded_msg = saved_img.decode_image()
        assert decoded_msg == test_message

class TestUtilities:

    def test_convert_message(self):

        test_message = 'the quick brown fox jumps over the lazy dog'
        test_list = []
        
        for i in test_message:
            # create a binary list representing the test message
            test_list.append(format(ord(i), '08b'))
        
        # use the utility to convert the message
        bin_list = convert_message(test_message)
        
        # assert they are the same
        assert bin_list == test_list

class TestFileIO:

    def test_file_input_exception(self):
        """
        design this to test to check that non-image files throw an exception
        and image files do not throw an exception
        """
        pass
