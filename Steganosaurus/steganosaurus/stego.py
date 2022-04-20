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
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty
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
        # Schedule the function call to update image,
        # remaning and maximum_char_count and text field.
        Clock.schedule_interval(self.update_main_widgets, .1) 
    
    # Use enum to define different message types.
    MESSAGE_TYPE = Enum('MESSAGE_TYPE', 'INFO ERROR WARNING SAVED')
    WARNING_TYPE = Enum('WARNING_TYPE', 'WARNINGSAVE RESET')
    user_notification_msg = StringProperty('Display Text Field Related Warning Message')
    warning_type = ''
    # this is the object to be referenced by all other functions
    # initialize with the default constructor
    display_image = ImageObject()
    maximum_char_count = NumericProperty(display_image.max_available_chars)
    textfield_str = StringProperty(display_image.decode_image())

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
        
        if message_type == self.MESSAGE_TYPE.INFO or message_type == self.MESSAGE_TYPE.ERROR:
            App.get_running_app().message_type = 'Info/Error'
            Factory.InfoAndErrorPopup().open()
        # for saving
        if message_type == self.WARNING_TYPE.WARNINGSAVE:
            App.get_running_app().message_type = 'Warning'
            Factory.InfoAndErrorPopup().open()

        if message_type == self.MESSAGE_TYPE.SAVED:
            App.get_running_app().message_type = 'Info/Error'
            Factory.InfoAndErrorPopup().open()

    def on_open_button_click(self):
        """Call the method show_load_list() to open the file chooser dialog."""
        self.display_image = ImageChooserPopup().show_load_list()

    def on_encode_button_click(self):
        """Call the method encode_image() and enable the reset button."""
        # Passing text field input to ecode method.
        MainWidget.display_image.encode_image(self.ids.main_text_field.text)
        # Only enable reset button, after successfully encoding the image.
        App.get_running_app().reset_btn_disabled = False
        # After finidhing encoding, disable the textfield modification.
        App.get_running_app().textfield_disabled = True


        # Set reset button warning popup values.
        # self.warning_type = self.WARNING_TYPE.SAVE
        # self.popup_user_notification( \
        #    'Are you sure you want to overwrite the image?', self.MESSAGE_TYPE.WARNING)

    def on_reset_button_click(self):
        """Popup warning dialog."""
        # Set reset button warning popup values.
        self.warning_type = self.WARNING_TYPE.RESET
        self.popup_user_notification( \
            'Are you sure you want to reset the image?', self.MESSAGE_TYPE.WARNING)

    def execute_reset(self):
        """Call the method reset_image()"""    
        MainWidget.display_image.reset_image()

    def update_warning_btn_yes(self, warning_btn_yes):
        """
        If the user click "yes" on the warning dialog,
        disable the reset button and call the method execute_reset/execute_save;
        otherwise, do nothing.
        The method is called from dialog.kv file.
        """
        if warning_btn_yes:
            if self.warning_type == self.WARNING_TYPE.RESET:
                self.update_textfield_input() # Reset the textfield.
                self.execute_reset()
                App.get_running_app().reset_btn_disabled = True
                App.get_running_app().textfield_disabled = False

            if self.warning_type == self.WARNING_TYPE.WARNINGSAVE: # TODO: Save image popup
                #self.execute_save()
                # After successfully saving the image, disable reset button
                # and enable the text field.
                App.get_running_app().reset_btn_disabled = True
                App.get_running_app().textfield_disabled = False
                self.ids.main_text_field.text = '' # Clear text field.
        else:
            if self.warning_type == self.WARNING_TYPE.RESET:
                App.get_running_app().reset_btn_disabled = False

    def update_main_widgets(self, *args):
        """
        Update the main GUI widgets(image source, 
        remaining and maximum_char_count) values and
        assign new decoded image message to the variable self.textfield_str.
        """
        self.ids.main_image.source = MainWidget.display_image.filename
        self.ids.input_char_count.text = "(" \
            + (str(MainWidget.display_image.max_available_chars - len(self.ids.main_text_field.text))) \
            + "/" + str(MainWidget.display_image.max_available_chars) +")"
        self.textfield_str = MainWidget.display_image.decode_image()

    def update_textfield_input(self):
        """
        Assign the value of self.textfield_str 
        to the main GUI TextField text attribute.
        """
        self.ids.main_text_field.text = self.textfield_str

    # when user presses enter, maybe link this to encode button?
    def on_text_validate(self):
        pass

    def on_save_button_click(self):
        """ check if GUI has image loaded"""
        try:
            # check if the image is loaded onto the screen
            # which means an image was chosen
            if not MainWidget.display_image is None:
                print("*** MainWidget.on_save_button_click() data check ***\n")
                print(f"Image loaded {MainWidget.display_image.filename}\n")
                print(f"Image type {type(MainWidget.display_image.filename)}\n")
                # get the file path
                """Call the method show_load_list() to open the file chooser dialog."""
                ImageSaverPopup().show_filechooser()
            else:
                print("image not loaded\n")
                raise Exception
        except Exception:
            MainWidget.popup_user_notification(MainWidget(),'Please select a valid image file to save', MainWidget.MESSAGE_TYPE.INFO)

# global file_path to be shared between ImageSaverPopup and ImageChooserPopup for saving
class ImageSaverPopup(Popup):
    # local to hold current path directory where image can be saved
    save_dir: str = ''
    # I am pretty sure this method should be fired whenever the user clicks on a folder
    def folder_clicked(self,path,filename):
        """called by ImageChooserPopup Widget in mainframe.kv"""
        try:
            print("*** ImageSaverPopup.folder_clicked() data check ***\n")
            with open(os.path.join(path, filename[0])) as stream:
                self.text_input.text = stream.read()

        except:
            pass # TODO: Specify Exceptions

    def show_filechooser(self):
        print("*** ImageSaverPopup.show_filechooser() data check ***\n")
        print("Image Saver Popup opened\n")
        print(f"File path string {MainWidget.display_image.filename}\n")
        im = Image.open(MainWidget.display_image.filename)
        # if it is an image, verify if the image is not corrupted
        im.verify()
        print(f"Image {im}\n")
        Factory.ImageSaverPopup().open()

    def save(self):
        """On save button, file saved here"""
        try:
            print(f"File path string {MainWidget.display_image.filename}\n")
            # dismiss popup after saving
            self.dismiss()
            # verify user wants to save 
            # Zhihua can you explain the popups I had trouble implementing them correctly they are kind of confusing
            # There will be 3 popups for saving:

            # the first is a warning in case of overwriting yes no dialog

            # the second is a warning just to double check if they really want to save, yes no dialog

            # the third dialog will an info popup when the user tries to save in an unauthorized location. I'll add 
            # the logic to that soon

            # MainWidget.popup_user_notification(MainWidget(),'Image successfully Saved!', MainWidget.WARNING_TYPE.WARNINGSAVE)
            # MainWidget.popup_user_notification(MainWidget(),'Image successfully Saved!', MainWidget.MESSAGE_TYPE.SAVED)
        # throw a "not an image" popup
        except Exception:
            MainWidget.popup_user_notification(MainWidget(),'Please select a valid image file.', MainWidget.MESSAGE_TYPE.INFO)

class ImageChooserPopup(Popup):

    file_path: str = ''
    def show_load_list(self):
        Factory.ImageChooserPopup().open()

    def selected(self,filename):
        """called by ImageChooserPopup Widget in mainframe.kv"""
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

        except:
            pass # TODO: Specify Exceptions

    def load_list(self):
        """On load button, file processed here"""
        # check whether this image is actually an image or not
        # when load button is pressed
        try:
            print(f"File path string {self.file_path}\n")
            im = Image.open(self.file_path)
            # if it is an image, verify if the image is not corrupted
            im.verify()
            # assign to display_image in main window
            MainWidget.display_image = ImageObject(filename=self.file_path)
            # After successfully uploades image, disable the reset button
            # and enable the textfield.     
            App.get_running_app().reset_btn_disabled = True
            App.get_running_app().textfield_disabled = False

            # refresh window
            # print(MainWidget.display_image.filename)
            # dismiss popup
            self.dismiss()
        # throw a "not an image" popup
        except Exception:
            MainWidget.popup_user_notification(MainWidget(),'Please select a valid image file.', MainWidget.MESSAGE_TYPE.INFO)

    


    def dismiss_popup(self):
        pass


class MainFrame(App):

    message = ''
    message_type = ''
    reset_btn_disabled = BooleanProperty(True)
    textfield_disabled = BooleanProperty(False)

    # use this path to load logo images
    LOGO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/stego.png'))

    def build(self):
        self.title = 'Steganosaurus' # GUI title.
        return MainWidget()

MainFrame().run()