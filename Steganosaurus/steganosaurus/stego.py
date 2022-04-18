"""
Steganosaurus
    
Linden Crandall
Jonthan Mainhart
Zhihua Zheng

Final Project for CMSC 495.

April 12, 2022

MainFrame classes for Steganosaurus.
"""
from kivy.config import Config
# Set window non-resizable, before creating the window.
# Don't change the position of this code.
Config.set('graphics', 'resizable', False)

import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout  import GridLayout
from kivy.uix.floatlayout  import FloatLayout
from kivy.lang import Builder
from kivy.config import Config
from kivy.factory import Factory
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.uix.popup import Popup
from models import ImageObject
from kivy.clock import Clock
from kivy.core.window import Window
from enum import Enum
# import PIL for image processing
from PIL import Image

# Set window size.
Window.size = (550, 500)
# Import external kv file.
Builder.load_file(os.path.abspath(os.path.join(os.path.dirname(__file__), 'dialog.kv')))

class MainWidget(GridLayout):
    def __init__(self, **kwargs):  #kivy constructor takes 2 arguments.
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_image, .1) # Schedule the function call.
    
    # Use enum to define different message types.
    MESSAGE_TYPE = Enum('MESSAGE_TYPE', 'INFO ERROR WARNING')
    user_notification_msg = StringProperty('Display Text Field Related Warning Message')
    textfield_str = StringProperty('')

    # this is the object to be referenced by all other functions
    # initialize with the default constructor
    display_image = ImageObject()
    maximum_char_count = NumericProperty(display_image.max_available_chars)

    def popup_user_notification(self, message, message_type):
        """Displays user notification popup dialog.
        
        Args:
            message: the text message will be displayed.
            message_type: enum 
        """
        App.get_running_app().message = message # Assign popup message.
        if message_type == self.MESSAGE_TYPE.WARNING: # Validate message type.
            App.get_running_app().message_type = 'Warning' # Assign message type.
            Factory.WarningPopup().open()
        
        if message_type == self.MESSAGE_TYPE.INFO or message_type == self.MESSAGE_TYPE.ERROR:
            App.get_running_app().message_type = 'Info/Error'
            Factory.InfoAndErrorPopup().open()

    def on_open_button_click(self):
        """Call the method show_load_list() to open the file chooser dialog."""
        self.display_image = FileChooserPopup().show_load_list()

    def on_encode_button_click(self):
        """Call the method encode_image() and enable the reset button."""
        MainWidget.display_image.encode_image(MainWidget.display_image.filename)
        # Only enable reset button, after successfully encoding the image.
        App.get_running_app().reset_btn_disabled = False
        # Set reset button warning popup values.
        App.get_running_app().message = 'Are you sure you want to reset the image?'
        App.get_running_app().message_type = 'Warning'
        
    def on_save_button_click(self):
        """Call the method save_image() and disable the reset button."""
        # TODO: Call the save image function.
        print("TODO: Call the save image function.")
        # After successfully saving the image, disable reset button.
        App.get_running_app().reset_btn_disabled = BooleanProperty(True)

    def on_reset_button_click(self):
        """If the user click "yes" on the warning dialog disable the reset button
        and call the method rest_image(); otherwise, do nothing.
        This method is called from dialog.kv file"""
        MainWidget.display_image.reset_image()
        # After successfully resetting the image, disable reset button.
        App.get_running_app().reset_btn_disabled = BooleanProperty(True)
        
    def update_image(self, *args):
        # Update the image source.
        self.ids.main_image.source = MainWidget.display_image.filename


class FileChooserPopup(Popup):

    file_path: str = ''

    def show_load_list(self):
        Factory.FileChooserPopup().open()

    def selected(self,filename):
        """called by FileChooserPopup Widget in mainframe.kv"""
        try:
            # setting this item to a list, the 0th item in the list
            # which is the filename
            # from mainframe.kv file
            # Image:
            #   id: file_image
            #   source: ""
            # NOTE: set on file click, not load button click
            self.ids.file_image.source = filename[0]
            # assign to local
            self.file_path = os.path.abspath(filename[0])

        except:
            pass # TODO: Specify Exceptions

    def load_list(self):
        """On load button, file processed here"""
        # check whether this image is actually an image or not
        # when load button is pressed
        try:
            im = Image.open(self.file_path)
            # if it is an image, verify if the image is not corrupted
            im.verify()
            # assign to display_image in main window
            MainWidget.display_image = ImageObject(filename=self.file_path)
            # After successfully uploaded image, disable the reset button.
            App.get_running_app().reset_btn_disabled = BooleanProperty(True)
            # refresh window
            print(MainWidget.display_image.filename)

            # dismiss popup
            self.dismiss()
        # throw a "not an image" popup, using pass for now until Zhihua completes method
        except Exception:
            pass
            # MainWidget.popup_user_notification(self,"Invalid file, please choose a valid image" +
            # " file ending with .jpg,.jpeg, or .png", "ERROR")  

    def dismiss_popup(self):
        pass

    # saving the image
    def save_image_to_machine(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()

class MainFrame(App):

    message = ''
    message_type = ''
    reset_btn_disabled = BooleanProperty(True)

    # use this path to load logo images
    LOGO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/stego.png'))

    def build(self):
        self.title = 'Steganosaurus' # GUI title.
        return MainWidget()

MainFrame().run()