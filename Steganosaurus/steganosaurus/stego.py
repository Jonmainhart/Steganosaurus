"""
Steganosaurus
    
Linden Crandall
Jonthan Mainhart
Zhihua Zheng

Final Project for CMSC 495.

April 12, 2022

MainFrame classes for Steganosaurus.
"""
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout  import GridLayout
from kivy.uix.floatlayout  import FloatLayout
from kivy.lang import Builder
from kivy.config import Config
from kivy.factory import Factory
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.popup import Popup
from models import ImageObject
from kivy.clock import Clock
from kivy.core.window import Window

# Set window size.
Window.size = (500, 500)
# Import external kv file.
Builder.load_file(os.path.abspath(os.path.join(os.path.dirname(__file__), 'dialog.kv')))

class MainWidget(GridLayout):
    def __init__(self, **kwargs):  #kivy constructor takes 2 arguments.
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_image, .1) # Schedule the function call.

    # use this path to load logo images
    LOGO_PATH = os.path.abspath('assets/stego.png')
    
    reset_btn_disabled = BooleanProperty(True)
    user_notification_msg = StringProperty('Display Text Field Related Warning Message')
    textfield_str = StringProperty('')
    maximum_char_count = StringProperty('0')

    # this is the object to be referenced by all other functions
    # initialize with the default constructor
    display_image = ImageObject()
    maximum_char_count = str(display_image.max_available_chars)

    def popup_user_notification(self, message, message_type):

        # TODO: Replace with validating message_type
        if self.get_id(message) == '"temporary_btn_id2"':
            App.get_running_app().message = 'Warning Message!'
            App.get_running_app().message_type = 'Warning'
            Factory.WarningPopup().open()
        else:
            App.get_running_app().message = 'Info/Error Message'
            App.get_running_app().message_type = 'Info/Error'
            Factory.InfoAndErrorPopup().open()

    def on_open_button_click(self):
        self.display_image = FileChooserPopup().show_load_list()

    def on_encode_button_click(self):
        # TODO: If encode button is clicked/done
        # reset_btn_disabled = BooleanProperty(False)
        pass

    def on_save_button_click(self):
        pass
        # print("Save Image button is clicked")

    def on_reset_button_click(self):
        print("Reset Image button is clicked")

    def update_image(self, *args):
        # Update the image source.
        self.ids.main_image.source = MainWidget.display_image.filename

    # Temporary function to get widget id from mainframe.
    # To display different popup windows.
    def get_id(self,  obj):
        for id, widget in self.ids.items():
            if widget.__self__ == obj:
                return id

class FileChooserPopup(Popup):

    file_path: str = ''

    def show_load_list(self):
        Factory.FileChooserPopup().open()

    def selected(self,filename):
        try:
            self.ids.file_image.source = filename[0]
            # assign to local
            # TODO: After clicking on multiple images then click load button NotADirectoryError occurs.
            self.file_path += os.path.abspath(filename[0])

        except:
            pass # TODO: Specify Exceptions

    def load_list(self):
        # assign to display_image in main window
        MainWidget.display_image = ImageObject(filename=self.file_path)
        # refresh window
        print(MainWidget.display_image.filename)

        # dismiss popup
        self.dismiss()

    def dismiss_popup(self):
        pass

class MainFrame(App):
    message = 'message'
    message_type = 'message_type'

    def build(self):
        self.title = 'Steganosaurus' # GUI title.
        return MainWidget()

MainFrame().run()