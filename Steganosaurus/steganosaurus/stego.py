"""
Steganosaurus
    
Linden Crandall
Jonthan Mainhart
Zhihua Zheng

Final Project for CMSC 495.

April 12, 2022

MainFrame classes for Steganosaurus.
"""
from xmlrpc.client import Boolean
from kivy.config import Config
# Set window non-resizable, before creating the window.
# Don't change the position of this code.
Config.set('graphics', 'resizable', False)

import os, platform, re
from kivy.app import App
from kivy.cache import Cache
from kivy.uix.gridlayout  import GridLayout
from kivy.lang import Builder
from kivy.config import Config
from kivy.factory import Factory
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.uix.popup import Popup
from models import ImageObject
from kivy.clock import Clock
from kivy.core.window import Window
from enum import Enum
from pathlib import Path
# import PIL for image processing
from PIL import Image

# Set window size.
Window.size = (550, 500)
# Import external kv file.
Builder.load_file(os.path.abspath(os.path.join(os.path.dirname(__file__), 'dialog.kv')))

class MainWidget(GridLayout):
    def __init__(self, **kwargs):  #kivy constructor takes 2 arguments.
        super().__init__(**kwargs)
        # Schedule the function call to update image,
        # remaning and maximum_char_count and text field.
        Clock.schedule_interval(self.update_main_widgets, .1) 
    
    # Use enum to define different message types.
    MESSAGE_TYPE = Enum('MESSAGE_TYPE', 'INFO ERROR WARNING')
    WARNING_TYPE = Enum('WARNING_TYPE', 'WARNINGSAVE RESET')
    # this is the object to be referenced by all other functions
    # initialize with the default constructor
    display_image = ImageObject()
    # Define local variables with default values.
    user_notification_msg = StringProperty('Note: Below displays the default decoded message.')
    warning_type, new_filepath, new_filename = '', '', ''
    encodable_bool = True
    maximum_char_count = NumericProperty(display_image.max_available_chars)
    textfield_str = StringProperty(display_image.decode_image())

    def on_open_button_click(self):
        """Call the method show_load_list() to open the file chooser dialog."""
        self.display_image = ImageChooserPopup().show_load_list()

    def on_encode_button_click(self):
        """
        Call the method encode_image() and enable the reset button,
        if the varaible encodable_bool is true;
        otherwise, popup warning message.
        """
        if (self.encodable_bool):
            # Passing the text field input to ecode method.
            MainWidget.display_image.encode_image(self.ids.main_text_field.text)
            # Enable reset button, disable the textfield modification.
            self.update_widgets_status(False, True, False)
        else:
            self.popup_user_notification('Failed to execute encode function!\
            \nPlease modify the text field input.', MainWidget.MESSAGE_TYPE.ERROR)

    def on_reset_button_click(self):
        """Popup reset warning dialog."""
        # Set reset button warning popup values.
        self.warning_type = self.WARNING_TYPE.RESET
        self.popup_user_notification( \
            'Are you sure you want to reset the image?', self.MESSAGE_TYPE.WARNING)

    def execute_reset(self):
        """Call the method reset_image()"""    
        MainWidget.display_image.reset_image()

    def on_save_button_click(self):
        """
        If the selected image is valid, call the method show_load_list() 
        to open the file saver dialog; otherwise, display error popup.
        """
        # Reset image saver popup dismiss status.
        App.get_running_app().image_saver_dismiss = False

        # check if the image is loaded onto the screen
        # which means an image was chosen
        if not MainWidget.display_image is None:
            if not self.new_filename: # Validate if new file name exists.
                # Assign current image file name.
                self.new_filename = App.get_running_app().current_filename
            ImageSaverPopup().show_filechooser()
        else:
            self.popup_user_notification('Please select a valid image file to save.'\
                , MainWidget.MESSAGE_TYPE.INFO)

    def save(self, new_filepath, new_filename):
        """
        If the new image name is valid, popup warning dialogs.
        Otherwise, do nothing.
        
        Args:
            new_filepath: String
            new_filename: String
        """  
        if (self.validate_image_name(new_filename)): # Validate the new input file name.
            try:
                self.new_filepath = new_filepath
                self.warning_type = self.WARNING_TYPE.WARNINGSAVE
                # Validate the extension of the file, if none exist, set default extension as PNG.
                if not ('.png' in new_filename.lower() or '.jpeg' in new_filename.lower()\
                    or '.jpg' in new_filename.lower()):
                    new_filename += '.png'
                
                self.new_filename = new_filename # Assign file name.

                # Validate if the user trying to overwrite image.
                if ((Path.cwd() / new_filepath / new_filename).exists()):
                    # Popup overwriting warning dialog
                    self.overwrite_bool = (self.popup_user_notification( 'Image name already exists.'\
                    '\nAre you sure you want to overwrite the image?', self.MESSAGE_TYPE.WARNING))
                else:
                    # Popup warning dialog, if proceed saving image or not.
                    self.overwrite_bool = (self.popup_user_notification( \
                    'Are you sure you want to save the image?', self.MESSAGE_TYPE.WARNING))

            except Exception:
                self.popup_user_notification('Please select a valid image file.', self.MESSAGE_TYPE.INFO)

    def execute_save(self):
        """
        Call external method save_image() to save the new encoded image.
        Then display saved image to the main gui, call decode_image()
        to display decoded message in the text field.
        """
        try:
            MainWidget.display_image.save_image(self.new_filepath, self.new_filename)
            App.get_running_app().title = 'Steganosaurus - ' + self.new_filename
            self.ids.main_image.source = self.new_filepath + '/' + self.new_filename # Upload saved image
            self.textfield_str = MainWidget.display_image.decode_image() # Decode saved image

        except PermissionError:
            MainWidget.popup_user_notification(MainWidget(),'Permission denied to access the file.',\
                MainWidget.MESSAGE_TYPE.ERROR)

        except Exception:
            MainWidget.popup_user_notification(MainWidget(),'Fail to save the file.',
                MainWidget.MESSAGE_TYPE.ERROR)

    def validate_image_name(self, image_name):
        """
        Validate the new image name, that the user entered in the textfield.
        File name only allows alphanumeric characters, underscore and hyphens.
        Underscore and hyphens are not allowed to be placed at the first or last position.
        Dot(.) in the middle of the image name is allowed to accept overwriting the existing image.
        
        Args:
            image_name: String
        """
        pattern = re.compile('^[A-Za-z0-9]+[\w\-.]+[^-_.]$')
        if pattern.match(image_name) is None:
            self.popup_user_notification("Invalid file name!\
            \nOnly alphabet characters, numbers, dot, underscore and hyphens are allowed. (e.g. image_1)\
            ", MainWidget.MESSAGE_TYPE.ERROR)
            return False
        return True

    def popup_user_notification(self, message, message_type):
        """
        Displays user notification popup dialog.
        
        Args:
            message: the text message will be displayed.
            message_type: enum 
        """
        App.get_running_app().message = message # Assign popup message.
        if message_type == self.MESSAGE_TYPE.WARNING: # Validate message type.
            App.get_running_app().message_type = 'Warning' # Assign message type.
            Factory.WarningPopup().open()
        
        if message_type == self.MESSAGE_TYPE.INFO:
            App.get_running_app().message_type = 'Info'
            Factory.InfoAndErrorPopup().open()
        
        if message_type == self.MESSAGE_TYPE.ERROR:
            App.get_running_app().message_type = 'Error'
            Factory.InfoAndErrorPopup().open()

    def update_warning_btn_yes(self, warning_btn_yes):
        """
        If the user click "yes" on the warning dialog,
        disable the reset button and call the method execute_reset/execute_save;
        otherwise, do nothing.
        The method is called from dialog.kv file.

        Args:
            warning_btn_yes: boolean
        """
        if warning_btn_yes:
            if self.warning_type == self.WARNING_TYPE.RESET: # Reset image popup.
                self.update_textfield_input() # Reset the textfield.
                self.execute_reset()
                # Enable reset button and enable the text field.
                self.update_widgets_status(True, False, False)

            if self.warning_type == self.WARNING_TYPE.WARNINGSAVE: # Save image popup.
                self.execute_save()
                # Enable reset button, enable the text field and dismiss saver popup.
                self.update_widgets_status(True, False, True)
        else:
            if self.warning_type == self.WARNING_TYPE.RESET:
                # Enable reset button and enable the text field.
                self.update_widgets_status(False, True, False)

    def update_widgets_status(self, reset_btn_disabled, textfield_disabled, image_saver_dismiss):
        """
        Set Main GUI widgets' status enable/disabled.
        
        Args:
            reset_btn_disabled: boolean
            textfield_disabled: boolean
            image_saver_dismiss: boolean
        """
        App.get_running_app().reset_btn_disabled = reset_btn_disabled
        App.get_running_app().textfield_disabled = textfield_disabled
        App.get_running_app().image_saver_dismiss = image_saver_dismiss

    def update_main_widgets(self, *args):
        """
        Update the main GUI widgets(image source, MessageLabel
        and remaining and maximum_char_count) values, 
        assign new decoded image message to the variable self.textfield_str.
        """
        self.ids.main_image.source = MainWidget.display_image.filename
        self.textfield_str = MainWidget.display_image.decode_image()
        self.maximum_char_count = MainWidget.display_image.max_available_chars
        if ((len(self.ids.main_text_field.text) == 0)):
            self.user_notification_msg = ''
            self.encodable_bool = True
        elif((MainWidget.display_image.max_available_chars - len(self.ids.main_text_field.text) == 0)):
            self.user_notification_msg = 'Warning: Maximum encode character number has been reached.'
            self.encodable_bool = True
        elif((MainWidget.display_image.max_available_chars - len(self.ids.main_text_field.text) < 0)):
            self.user_notification_msg ='Warning: Not encodable. '\
            'Maximum encode characters have exceeded by '\
            + str((len(self.ids.main_text_field.text) - MainWidget.display_image.max_available_chars))
            self.encodable_bool = False

    def update_textfield_input(self):
        """
        Assign the value of self.textfield_str 
        to the main GUI TextField text attribute.
        """
        self.ids.main_text_field.text = self.textfield_str

class ImageSaverPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Schedule the function call to close the saver popup.
        Clock.schedule_interval(self.dismiss_popup, .1) 

    def show_filechooser(self):
        """Open file saver popup view."""
        self.open()

    def dismiss_popup(self, *args):
        """If the variable image_saver_dismiss is true, close popup."""
        if App.get_running_app().image_saver_dismiss:
            self.dismiss()

class ImageChooserPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)	
        # Remove cache, to reload the changed image files in the file chooser
        Cache.remove('kv.image')	
        Cache.remove('kv.texture')	

    file_path: str = ''
    def show_load_list(self):
        """Open file chooser popup view."""
        self.open()

    def selected(self,filename):
        """called by ImageChooserPopup Widget in mainframe.kv"""
        if len(filename) > 0:
            try:
                # setting this item to a list, the 0th item in the list
                # which is the filename full path
                # from mainframe.kv file
                # Image:
                #   id: file_image
                #   source: ""
                # NOTE: set on file click, not load button click
                self.ids.file_image.source = filename[0]
                # assign to local
                self.file_path = os.path.abspath(filename[0])

            except PermissionError:
                MainWidget.popup_user_notification(MainWidget(),'Permission denied to access the file.',\
                    MainWidget.MESSAGE_TYPE.ERROR)

            except Exception: # throw a "not an image" popup
                MainWidget.popup_user_notification(MainWidget(),'Please select a valid image file.',\
                    MainWidget.MESSAGE_TYPE.ERROR)

    def load_list(self):
        """On load button, file processed here """
        # check whether this image is actually an image or not
        # when load button is pressed
        try:
            im = Image.open(self.file_path)
            # if it is an image, verify if the image is not corrupted
            im.verify()
            # assign to display_image in main window
            MainWidget.display_image = ImageObject(filename=self.file_path)
            
            # Update main GUI title with the new file name
            App.get_running_app().current_image = \
                str(((MainWidget.display_image.filename).split(App.get_running_app().file_spliter))[-1])
            App.get_running_app().title = 'Steganosaurus - '+ App.get_running_app().current_image
            
            # Disable the reset button band enable the textfield.
            App.get_running_app().reset_btn_disabled = True
            App.get_running_app().textfield_disabled = False

            # dismiss popup
            self.dismiss()

        except PermissionError:
            MainWidget.popup_user_notification(MainWidget(),'Permission denied to access the file.',\
                MainWidget.MESSAGE_TYPE.ERROR)
                
        except Exception: # throw a "not an image" popup
            MainWidget.popup_user_notification(MainWidget(),'Please select a valid image file.',\
                MainWidget.MESSAGE_TYPE.ERROR)

class MainFrame(App):

    main_title, message, message_type, file_spliter, current_filename = '', '', '', '', ''
    reset_btn_disabled = BooleanProperty(True)
    textfield_disabled = BooleanProperty(False)
    image_saver_dismiss = BooleanProperty(False)
    valid_image_name = BooleanProperty(True)

    if platform.system() == 'Windows': # Windows
        file_spliter = "\\"
        current_filename = str(((MainWidget.display_image.filename).split(file_spliter))[-1])
        # Windows dafault title, if the "\\" and "/" are mixed in the file path.
        if "/" in current_filename:
            current_filename = str(((MainWidget.display_image.filename).split("/"))[-1])
    else: # Mac os & linux
        file_spliter = "/"
        current_filename = str(((MainWidget.display_image.filename).split(file_spliter))[-1])

    # Assign Main GUI title with image file name.
    main_title = 'Steganosaurus - ' + current_filename 
    # use this path to load logo images
    LOGO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/stego.png'))

    def build(self):
        self.title = self.main_title # GUI title.
        return MainWidget()

MainFrame().run()