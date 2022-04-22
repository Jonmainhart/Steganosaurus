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

import os, platform
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
    WARNING_TYPE = Enum('WARNING_TYPE', 'WARNINGSAVE RESET ENCODE')
    user_notification_msg = StringProperty('Note: Below displays the default decoded message.')
    warning_type, new_filepath, new_filename = '', '', ''
    encodable_bool = True
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
        
        if message_type == self.MESSAGE_TYPE.INFO:
            App.get_running_app().message_type = 'Info'
            Factory.InfoAndErrorPopup().open()
        
        if message_type == self.MESSAGE_TYPE.ERROR:
            App.get_running_app().message_type = 'Error'
            Factory.InfoAndErrorPopup().open()

    def on_open_button_click(self):
        """Call the method show_load_list() to open the file chooser dialog."""
        # Set back the default message 
        self.display_image = ImageChooserPopup().show_load_list()

    def on_encode_button_click(self):
        """Call the method encode_image() and enable the reset button."""
        if (self.encodable_bool):
            # Passing text field input to ecode method.
            MainWidget.display_image.encode_image(self.ids.main_text_field.text)
            # Only enable reset button, after successfully encoding the image.
            App.get_running_app().reset_btn_disabled = False
            # After finidhing encoding, disable the textfield modification.
            App.get_running_app().textfield_disabled = True
        else:
            self.popup_user_notification('Failed to execute encode function!\
            \nPlease modify the text field input.', MainWidget.MESSAGE_TYPE.ERROR)

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
                self.execute_save()
                App.get_running_app().image_saver_dismiss = True
                # After successfully saving the image, disable reset button
                # and enable the text field.
                App.get_running_app().reset_btn_disabled = True
                App.get_running_app().textfield_disabled = False
            if self.warning_type == self.WARNING_TYPE.ENCODE:
                self.on_encode_button_click()
        else:
            if self.warning_type == self.WARNING_TYPE.RESET:
                App.get_running_app().reset_btn_disabled = False

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

    def on_text_validate(self):
        """
        Display encode warning dialog, when user presses enter in the textfield.
        """
        self.warning_type = self.WARNING_TYPE.ENCODE
        # Popup overwriting warning dialog
        self.overwrite_bool = (self.popup_user_notification( \
        'Are you sure you want to encode the image?', self.MESSAGE_TYPE.WARNING))
    
    def on_save_button_click(self):
        """When the save button is clicked from the main menu on GUI"""
        App.get_running_app().image_saver_dismiss = False
        # check if GUI has image loaded
        try:
            # check if the image is loaded onto the screen
            # which means an image was chosen
            if not MainWidget.display_image is None:
                # get the file path
                """Call the method show_load_list() to open the file chooser dialog."""
                ImageSaverPopup().show_filechooser()
            else:
                raise Exception
        except Exception:
            self.popup_user_notification('Please select a valid image file to save', MainWidget.MESSAGE_TYPE.INFO)

    def save(self, new_filepath, new_filename):
        """On save button from the save filechooser, file saved to user's machine
        called by <ImageSaverPopup> in mainframe.kv line 213
        params: @new_filepath ->  FileChooserIconView.path in mainframe.kv line 197 which is assigned './' line 
         INDEXERROR HAPPENING HERE -> @new_filename -> FileChooserIconView.onselection in mainframe.kv line 198 assigned to
                 textinput.id line new_image_name """
        try:
            self.new_filepath = new_filepath
            self.warning_type = self.WARNING_TYPE.WARNINGSAVE
            if not ('.png' in new_filename.lower() or '.jpeg' in new_filename.lower() or '.jpg' in new_filename.lower()):
                new_filename += '.png'
            # Validate if the user trying to overwrite image.
            if ((Path.cwd() / new_filepath / new_filename).exists()):
                self.new_filename = new_filename.replace("overwriting: ", '')
                # Popup overwriting warning dialog
                self.overwrite_bool = (self.popup_user_notification( 'Image name already exists.\n'\
                'Are you sure you want to overwrite the image?', self.MESSAGE_TYPE.WARNING))
            else:
                self.new_filename = new_filename
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
        MainWidget.display_image.save_image(self.new_filepath, self.new_filename)
        App.get_running_app().title = 'Steganosaurus - ' + self.new_filename
        self.ids.main_image.source = self.new_filepath + '/' + self.new_filename # Upload saved image
        self.textfield_str = MainWidget.display_image.decode_image() # Decode saved image

# global file_path to be shared between ImageSaverPopup and ImageChooserPopup for saving
class ImageSaverPopup(Popup):
    def __init__(self, **kwargs):  #kivy constructor takes 2 arguments.
        super().__init__(**kwargs)
        # Schedule the function call to close the saver popup.
        Clock.schedule_interval(self.dismiss_popup, .1) 

    # local to hold current path directory where image can be saved
    save_dir: str = ''

    def show_filechooser(self):
        im = Image.open(MainWidget.display_image.filename)
        # if it is an image, verify if the image is not corrupted
        im.verify()
        self.open()

    def dismiss_popup(self, *args):
        if App.get_running_app().image_saver_dismiss:
            self.dismiss()

    def item_selected(self,filename):
        """ called by ImageSaverPopup Widget in mainframe.kv line 198 """
        try:
            print("Current image file to be saved: " + MainWidget.display_image.filename)
            print("Filename: " + filename[0])

        except:
            pass # TODO: Specify Exceptions

class ImageChooserPopup(Popup):
    def __init__(self, **kwargs):  #kivy constructor takes 2 arguments.	
        super().__init__(**kwargs)	
        # Remove cache, to reload the changed image files in the file chooser
        Cache.remove('kv.image')	
        Cache.remove('kv.texture')	

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

    # update Mainframe main_title with new image string found in MainWidget.display_image.filename
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
            App.get_running_app().title = 'Steganosaurus - ' \
                + str(((MainWidget.display_image.filename).split(App.get_running_app().file_spliter))[-1])
            # After successfully uploades image, disable the reset button
            # and enable the textfield.     
            App.get_running_app().reset_btn_disabled = True
            App.get_running_app().textfield_disabled = False
            # dismiss popup
            self.dismiss()
        # throw a "not an image" popup
        except Exception:
            MainWidget.popup_user_notification(MainWidget(),'Please select a valid image file.', MainWidget.MESSAGE_TYPE.INFO)

    def dismiss_popup(self):
        pass

class MainFrame(App):

    main_title, message, message_type, file_spliter = '', '', '', ''
    reset_btn_disabled = BooleanProperty(True)
    textfield_disabled = BooleanProperty(False)
    image_saver_dismiss = BooleanProperty(False)

    if platform.system() == 'Darwin': # Mac os
        file_spliter = "/"
    else: # windows & linux
        file_spliter = "\\"
    # Display Main Gui title with image file name.
    main_title = 'Steganosaurus - ' + str(((MainWidget.display_image.filename).split(file_spliter))[-1])
    
    # use this path to load logo images
    LOGO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/stego.png'))

    def build(self):
        self.title = self.main_title # GUI title.
        return MainWidget()

MainFrame().run()