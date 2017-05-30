from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.popup import Popup
from kivy.uix.label import Label

import os


def find_all_books(base_folder):
    '''return all Ebook path'''
    file_list = []
    for root, dirs, files in os.walk(base_folder, topdown=False): # find all files
        for name in files:
            path = os.path.join(root, name)
            #print(path)
            if path.split('.')[-1] in ['pdf', 'epub', 'mobi']:
                file_list.append(path)
        for name in dirs:
            pass
    if len(file_list) == 0: # if no file frond, show the current folder path
        file_list.append(base_folder)
    return file_list


# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<HomeScreen>:
    name: 'Home'
    GridLayout:
        cols: 1
        Button:
            text: 'Show All Ebooks'
            on_release: root.manager.current = 'Show'
            size_hint_y: 0.7
            pos_hint: {"left": 0, "top":1}
        Button:
            id: collect_button
            text: 'Collect All Ebooks to One Folder'
            on_release: root.manager.collect()
            size_hint_y: 0.3
            pos_hint: {"left": 0, "top":0.5}

<ShowScreen>:
    name: 'Show'
    RecycleView:
        data: [{'text': name} for name in root.manager.all_books_name]
        viewclass: 'Label'
        RecycleBoxLayout:
            default_size: None, dp(37)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
    Button:
        text: 'Back Home'
        on_release: root.manager.current = 'Home'
        size_hint: 1, 0.2
        pos_hint: {"bottom":1}

<RootWidget>:
    HomeScreen:
    ShowScreen:
""")


# Declare both screens
class HomeScreen(Screen):
    pass


class ShowScreen(Screen):
    pass


# Create the screen manager
class RootWidget(ScreenManager):
    def __init__(self, **kwargs):
        self.base_folder =os.path.dirname(os.path.abspath('.'))
        self.all_books_path = find_all_books(self.base_folder)
        self.all_books_name = [os.path.basename(name) for name in self.all_books_path] # Why can't get this from .kv file?
        
        super(RootWidget, self).__init__(**kwargs)

    def collect(self):
        '''collect all books to one folder'''
        if self.all_books_path[0] != self.base_folder: # detect if no books found
            goal_folder = os.path.join(self.base_folder, 'Books')
            if not os.path.exists(goal_folder): # if no goal_folder exists, creat a new one
                os.mkdir(goal_folder)
            for path in self.all_books_path: # move file
                goal_path = os.path.join(goal_folder, os.path.basename(path))
                os.rename(path, goal_path)
            Popup(title='Tip', content=Label(text='All Ebooks collected in \n'+goal_folder), size_hint=(None, None) ,size=(350, 350)).open()
            self.get_screen('Home').ids['collect_button'].text = 'Exit'
            self.get_screen('Home').ids['collect_button'].bind(on_release = exit)


class Collecter(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    Collecter().run()
