"""
Steganosaurus
    
Linden Crandall
Jonthan Mainhart
Zhihua Zheng

Final Project for CMSC 495.

April 12, 2022

MainFrame classes for Steganosaurus.
"""
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

# Set window size.
Config.set('graphics', 'width', '550')
Config.set('graphics', 'height', '500')
Config.set('graphics', 'resizable', False)
# Import external kv file.
Builder.load_file('dialog.kv')

class FileChooserPopup(Popup):

    display_image = ImageObject()

    def show_load_list(self):
        Factory.FileChooserPopup().open()

    def selected(self,filename):
        try:
            # Assign selected file path to image source.
            self.ids.file_image.source = filename[0] 
            # Pass selected file path to the ImageObject.
            self.display_image = ImageObject(filename[0])
            print(self.display_image) # TODO: Just to check the output. Delete later.
        except:
            pass # TODO: Specify Exceptions

    def load_list(self):
        pass

    def dismiss_popup(self):
        pass

class MainWidget(GridLayout):

    reset_btn_disabled = BooleanProperty(True)
    user_notification_msg = StringProperty('Display Text Field Related Warning Message')
    textfield_str = StringProperty('')
    maximum_char_count = StringProperty('100')

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
        #print(str(MainFrame().message))

    def on_open_button_click(self):
        FileChooserPopup().show_load_list()

    def on_encode_button_click(self):
        # TODO: If encode button is clicked/done
        # reset_btn_disabled = BooleanProperty(False)
        pass

    def on_save_button_click(self):
        pass
        # print("Save Image button is clicked")

    def on_reset_button_click(self):
        print("Reset Image button is clicked")

    # Temporary function to get widget id from mainframe.
    # To display different popup windows.
    def get_id(self,  obj):
        for id, widget in self.ids.items():
            if widget.__self__ == obj:
                return id

class MainFrame(App):
    message = 'message'
    message_type = 'message_type'
    def build(self):
        self.title = 'Steganosaurus' # GUI title.
        return MainWidget()

MainFrame().run()