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

class Model:

    def __init__(self):
        self.test_image = ImageObject(filename=path.abspath(path.join(path.dirname(__file__), '../../assets/300.jpeg')))
        self.test_message = 'the quick brown fox jumps over the lazy dog'

class TestModel:

    def test_max_char(self):
        img = Model()
        assert img.test_image.max_available_chars == 30000

    def test_encode_image(self):
        img = Model()
        img.test_image.encode_image(img.test_message)
        assert img.test_image.decode_image() == img.test_message

    def test_decode_image(self):
        img = Model()
        message = img.test_image.decode_image()
        assert message != img.test_message

