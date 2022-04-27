"""
Steganosaurus
    
Linden Crandall
Jonthan Mainhart
Zhihua Zheng

Final Project for CMSC 495.

April 26, 2022

Unit tests for Stenganosaurus application(stego.py).

Reference: https://github.com/KeyWeeUsr/KivyUnitTest
           https://pypi.org/project/kivyunittest/
"""
import unittest
import sys
import time
import os.path as op
from functools import partial
from kivy.clock import Clock
from unittest.mock import MagicMock, patch
from pathlib import Path
from kivy.core.window import Window

main_path = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(main_path)
from stego import MainFrame

class TestStego(unittest.TestCase):

    # sleep function that catches `dt` from Clock
    def pause(*args):
        time.sleep(0.1)

    # main test function
    def run_test_on_open_button_click(self, app, *args, MockClass):
        '''
        Open Image button test.
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.display_image = MagicMock()
        result = MockClass().show_load_list()
        # Execute.
        app.root.ids.open_btn.dispatch('on_release')
        # Validate.
        self.assertEqual(app.root.display_image, result)
        # End app.
        app.stop()
        Window.close()

    def run_test_on_encode_button_click_true(self, app, *args):
        '''
        Encode Image button test.
        condition: self.encodable_bool = True
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.display_image.encode_image = MagicMock()
        app.root.update_widgets_status = MagicMock()
        app.root.encodable_bool = True
        # Execute.
        app.root.ids.encode_btn.dispatch('on_release')
        # Validate.
        app.root.display_image.encode_image.assert_called_once_with(app.root.ids.main_text_field.text)
        app.root.update_widgets_status.assert_called_once_with(False, True, False)
        # End app.
        app.stop()
        Window.close()

    def run_test_on_encode_button_click_false(self, app, *args):
        '''
        Encode Image button test.
        condition: self.encodable_bool = False
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.popup_user_notification = MagicMock()
        app.root.encodable_bool = False
        # Execute.
        app.root.ids.encode_btn.dispatch('on_release')
        # Validate.
        app.root.popup_user_notification.assert_called_once_with('Failed to execute encode function!\
            \nPlease modify the text field input.', app.root.MESSAGE_TYPE.ERROR)
        # End app.
        app.stop()
        Window.close()

    def run_test_on_reset_button_click(self, app, *args):
        '''
        Rest Image button test.
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        expected = app.root.WARNING_TYPE.RESET
        app.root.popup_user_notification = MagicMock()
        # Execute.
        app.root.ids.reset_btn.dispatch('on_release')
        # Validate.
        self.assertEqual(expected, app.root.warning_type)
        app.root.popup_user_notification.assert_called_once_with(\
            'Are you sure you want to reset the image?', app.root.MESSAGE_TYPE.WARNING)
        # End app.
        app.stop()
        Window.close()
    
    def run_test_execute_reset(self, app, *args):
        '''
        execute_reset method test.
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.display_image.reset_image = MagicMock()
        # Execute.
        app.root.execute_reset()
        # Validate.
        app.root.display_image.reset_image.assert_called_once()
        # End app.
        app.stop()
        Window.close()

    def run_test_on_save_button_click(self, app, *args, MockClass):
        '''
        Save Image button test.
        condition:  (not MainWidget.display_image is None) == True
                    (not self.new_filename) = True
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.display_image = MagicMock(value="somestring")
        app.root.new_filename = ""
        app.current_filename = "expected"
        MockClass().show_filechooser = MagicMock()
        # Execute.
        app.root.ids.save_btn.dispatch('on_release')
        # Validate.
        self.assertEqual(app.current_filename, app.root.new_filename)
        MockClass().show_filechooser.assert_called_once()
        # End app.
        app.stop()
        Window.close()

    def run_test_on_save(self, app, *args):
        '''
        save method test.
        condition:  self.validate_image_name(new_filename) == True
                    (Path.cwd() / new_filepath / new_filename).exists()) = True
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.validate_image_name = MagicMock(return_value=True)
        new_filename = 'test_image_3.jpeg'
        new_filepath = main_path +  '/tests/'
        app.root.popup_user_notification = MagicMock()
        # Execute.
        app.root.save(new_filepath, new_filename)
        # Validate.
        app.root.popup_user_notification.assert_called_once_with('Image name already exists.'\
            '\nAre you sure you want to overwrite the image?', app.root.MESSAGE_TYPE.WARNING)
        # End app.
        app.stop()
        Window.close()

    def run_test_on_save_2(self, app, *args):
        '''
        save method test.
        condition:  self.validate_image_name(new_filename) == True
                    (Path.cwd() / new_filepath / new_filename).exists()) = False
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.validate_image_name = MagicMock(return_value=True)
        new_filename = 'test_no_image.png'
        new_filepath = main_path +  '/tests/'
        app.root.popup_user_notification = MagicMock()
        # Execute.
        app.root.save(new_filepath, new_filename)
        # Validate.
        app.root.popup_user_notification.assert_called_once_with(\
            'Are you sure you want to save the image?', app.root.MESSAGE_TYPE.WARNING)
        app.stop()
        Window.close()

    def run_test_execute_save(self, app, *args):
        '''
        execute_save method test.
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.display_image.save_image = MagicMock()
        app.root.display_image.decode_image = MagicMock(return_value="decoded_msg")
        app.root.new_filename = 'test_image_3.jpeg'
        app.root.new_filepath = 'path'
        # Execute.
        app.root.execute_save()
        # Validate.
        app.root.display_image.save_image.assert_called_once_with('path', 'test_image_3.jpeg')
        self.assertEqual('Steganosaurus - ' + app.root.new_filename, app.title)
        self.assertEqual('path/test_image_3.jpeg', app.root.ids.main_image.source)
        self.assertEqual('decoded_msg', app.root.textfield_str)
        app.stop()
        Window.close()

    def run_test_validate_image_name_true(self, app, *args):
        '''
        validate_image_name method test.
        condition: pattern.match(image_name) = True
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        image_name = 'test_image_3.jpeg'
        # Execute.
        result = app.root.validate_image_name(image_name)
        # Validate.
        self.assertEqual(True, result)
        app.stop()
        Window.close()

    def run_test_validate_image_name_false(self, app, *args):
        '''
        validate_image_name method test.
        condition: pattern.match(image_name) = False
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        image_name = '_test_image_3.jpeg'
        app.root.popup_user_notification = MagicMock()
        # Execute.
        result = app.root.validate_image_name(image_name)
        # Validate.
        app.root.popup_user_notification.assert_called_once_with("Invalid file name!\
            \nOnly alphabet characters, numbers, dot, underscore and hyphens are allowed. (e.g. image_1)\
            ", app.root.MESSAGE_TYPE.ERROR)
        self.assertEqual(False, result)
        app.stop()
        Window.close()

    def run_test_update_warning_btn_yes_1(self, app, *args):
        '''
        update_warning_btn_yes method test.
        condition: warning_btn_yes = True
                   self.warning_type == self.WARNING_TYPE.RESET is True
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.warning_type = app.root.WARNING_TYPE.RESET
        app.root.update_textfield_input = MagicMock()
        app.root.execute_reset = MagicMock()
        app.root.update_widgets_status = MagicMock()
        # Execute.
        app.root.update_warning_btn_yes(True)
        # Validate.
        app.root.update_textfield_input.assert_called_once()
        app.root.execute_reset.assert_called_once()
        app.root.update_widgets_status.assert_called_once_with(True, False, False)
        # End app.
        app.stop()
        Window.close()

    def run_test_update_warning_btn_yes_2(self, app, *args):
        '''
        update_warning_btn_yes method test.
        condition: warning_btn_yes = True
                   self.warning_type == self.WARNING_TYPE.WARNINGSAVE is True
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.warning_type = app.root.WARNING_TYPE.WARNINGSAVE
        app.root.execute_save = MagicMock()
        app.root.update_widgets_status = MagicMock()
        # Execute.
        app.root.update_warning_btn_yes(True)
        # Validate.
        app.root.execute_save.assert_called_once()
        app.root.update_widgets_status.assert_called_once_with(True, False, True)
        # End app.
        app.stop()
        Window.close()

    def run_test_update_warning_btn_yes_3(self, app, *args):
        '''
        update_warning_btn_yes method test.
        condition: warning_btn_yes = False
                   self.warning_type == self.WARNING_TYPE.RESET is True is True
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.warning_type = app.root.WARNING_TYPE.RESET
        app.root.update_widgets_status = MagicMock()
        # Execute.
        app.root.update_warning_btn_yes(False)
        # Validate.
        app.root.update_widgets_status.assert_called_once_with(False, True, False)
        # End app.
        app.stop()
        Window.close()

    def run_test_update_widgets_status(self, app, *args):
        '''
        update_widgets_status method test.
        condition: reset_btn_disabled = False
                   textfield_disabled = True
                   image_saver_dismiss = True
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Execute.
        app.root.update_widgets_status(False, True, True)
        # Validate.
        self.assertEqual(False, app.reset_btn_disabled)
        self.assertEqual(True, app.textfield_disabled)
        self.assertEqual(True, app.image_saver_dismiss)
        # End app.
        app.stop()
        Window.close()

    def run_test_update_main_widgets_1(self, app, *args):
        '''
        update_widgets_status method test.
        condition: (len(self.ids.main_text_field.text) == 0)
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.display_image.filename ="filename"
        app.root.display_image.decode_image = MagicMock(return_value="decoded_msg")
        app.root.display_image.max_available_chars = 100
        app.root.ids.main_text_field.text = ''
        # Execute.
        app.root.update_main_widgets()
        # Validate.
        self.assertEqual("filename", app.root.ids.main_image.source)
        self.assertEqual("decoded_msg", app.root.textfield_str)
        self.assertEqual(100, app.root.maximum_char_count)
        self.assertEqual(True, app.root.encodable_bool)
        # End app.
        app.stop()
        Window.close()

    def run_test_update_main_widgets_2(self, app, *args):
        '''
        update_widgets_status method test.
        condition: MainWidget.display_image.max_available_chars - len(self.ids.main_text_field.text) == 0
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.display_image.filename ="filename"
        app.root.display_image.decode_image = MagicMock(return_value="decoded_msg")
        app.root.display_image.max_available_chars = 11 # 'decoded_msg' length is 11.

        # Execute.
        app.root.update_main_widgets()
        # Validate.
        self.assertEqual("filename", app.root.ids.main_image.source)
        self.assertEqual("decoded_msg", app.root.textfield_str)
        self.assertEqual(11, app.root.maximum_char_count)
        self.assertEqual(\
             'Warning: Maximum encode character number has been reached.', app.root.user_notification_msg)
        self.assertEqual(True, app.root.encodable_bool)
        # End app.
        app.stop()
        Window.close()

    def run_test_update_main_widgets_3(self, app, *args):
        '''
        update_widgets_status method test.
        condition: MainWidget.display_image.max_available_chars - len(self.ids.main_text_field.text) < 0
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.display_image.filename ="filename"
        app.root.display_image.decode_image = MagicMock(return_value="decoded_msg")
        app.root.display_image.max_available_chars = 10 # 'decoded_msg' length is 11.
        # Execute.
        app.root.update_main_widgets()
        # Validate.
        self.assertEqual("filename", app.root.ids.main_image.source)
        self.assertEqual("decoded_msg", app.root.textfield_str)
        self.assertEqual(10, app.root.maximum_char_count)
        self.assertEqual(\
             'Warning: Not encodable. Maximum encode characters have exceeded by 1'\
                , app.root.user_notification_msg)
        self.assertEqual(False, app.root.encodable_bool)
        # End app.
        app.stop()
        Window.close()

    def run_test_update_textfield_input(self, app, *args):
        '''
        update_textfield_input method test.
        '''
        Clock.schedule_interval(self.pause, 0.000001)
        # Setup.
        app.root.textfield_str ="somestring"
        # Execute.
        app.root.update_textfield_input()
        # Validate.
        self.assertEqual("somestring", app.root.ids.main_text_field.text)
        # End app.
        app.stop()
        Window.close()

    @patch('stego.ImageChooserPopup')
    def test_on_open_button_click(self, MockClass):
        app = MainFrame()
        p = partial(self.run_test_on_open_button_click, app, MockClass = MockClass)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_on_encode_button_click_true(self):
        app = MainFrame()
        p = partial(self.run_test_on_encode_button_click_true, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_on_encode_button_click_false(self):
        app = MainFrame()
        p = partial(self.run_test_on_encode_button_click_false, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_on_reset_button_click(self):
        app = MainFrame()
        p = partial(self.run_test_on_reset_button_click, app)
        Clock.schedule_once(p, 0.000001)
        app.run()
    
    def test_execute_reset(self):
        app = MainFrame()
        p = partial(self.run_test_execute_reset, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    @patch('stego.ImageSaverPopup')
    def test_on_save_button_click(self, MockClass):
        app = MainFrame()
        p = partial(self.run_test_on_save_button_click, app, MockClass = MockClass)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_save (self):
        app = MainFrame()
        p = partial(self.run_test_on_save, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_save_2 (self):
        app = MainFrame()
        p = partial(self.run_test_on_save_2, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_execute_save (self):
        app = MainFrame()
        p = partial(self.run_test_execute_save, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_validate_image_name_true (self):
        app = MainFrame()
        p = partial(self.run_test_validate_image_name_true, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_validate_image_name_false (self):
        app = MainFrame()
        p = partial(self.run_test_validate_image_name_false, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_update_warning_btn_yes_1 (self):
        app = MainFrame()
        p = partial(self.run_test_update_warning_btn_yes_1, app)
        Clock.schedule_once(p, 0.000001)
        app.run()
    
    def test_update_warning_btn_yes_2 (self):
        app = MainFrame()
        p = partial(self.run_test_update_warning_btn_yes_2, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_update_warning_btn_yes_3 (self):
        app = MainFrame()
        p = partial(self.run_test_update_warning_btn_yes_3, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_update_widgets_status (self):
        app = MainFrame()
        p = partial(self.run_test_update_widgets_status, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_update_main_widgets_1 (self):
        app = MainFrame()
        p = partial(self.run_test_update_main_widgets_1, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_update_main_widgets_2 (self):
        app = MainFrame()
        p = partial(self.run_test_update_main_widgets_2, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_update_main_widgets_3 (self):
        app = MainFrame()
        p = partial(self.run_test_update_main_widgets_3, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

    def test_update_textfield_input (self):
        app = MainFrame()
        p = partial(self.run_test_update_textfield_input, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

if __name__ == '__main__':
    unittest.main()