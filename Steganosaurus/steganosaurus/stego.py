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
from kivy.lang import Builder
from kivy.config import Config
from kivy.factory import Factory

# Set window size.
Config.set('graphics', 'width', '550')
Config.set('graphics', 'height', '500')
# Import external kv file.
Builder.load_file('dialog.kv')

class MainWidget(Widget):

    def popup_user_notification(self, message, message_type):
        # TODO: Replace with validating message_type
        if self.get_id(message) == '"temporary_btn_id1"':
            Factory.WarningPopup().open()
        else:
            Factory.InfoAndErrorPopup().open()

    # Temporary function to get widget id from mainframe.
    # To display different popup windows.
    def get_id(self,  obj):
        for id, widget in self.ids.items():
            if widget.__self__ == obj:
                return id

class MainFrame(App):

    def build(self):
        self.title = 'Steganosaurus' # GUI title.
        self.message = 'message' # TODO: Reset the variable.
        self.message_type = 'message_type' # TODO: Reset the variable.
        return MainWidget()
MainFrame().run()