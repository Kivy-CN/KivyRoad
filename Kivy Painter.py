from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from kivy.uix.widget import Widget
from kivy.graphics import Line


class Painter(Widget):
   
   def on_touch_down(self, touch):
       with self.canvas:
           touch.ud["line"] = Line(points=(touch.x, touch.y))
           
   def on_touch_move(self, touch):
       touch.ud["line"].points += (touch.x, touch.y)


class MainScreen(Screen):
   pass

class AnotherScreen(Screen):
   pass

class ScreenManagement(ScreenManager):
   pass

presentation = Builder.load_string("""
#: import FadeTransition kivy.uix.screenmanager.FadeTransition

ScreenManagement:
    transition: FadeTransition()
    MainScreen:
    AnotherScreen:

<MainScreen>:
    name: "main"
    Button:
        on_release: root.manager.current = "other"
        text: "Next Screen"
        font_size: 50

<AnotherScreen>:
    name: "other"
    FloatLayout:
        Painter:
            id: painter
        Button:
            color: 0, 1, 0, 1
            font_size: 25
            size_hint: 0.3, 0.2
            text: "Back Home"
            on_release: root.manager.current = "main"
            pos_hint: {"right": 1, "top":1}
        Button:
            color: 0, 1, 0, 1
            font_size: 25
            size_hint: 0.3, 0.2
            text: "Clear"
            on_release: root.ids['painter'].canvas.clear()
            pos_hint: {"left": 0, "top":1}
""")


class SimpleKivy(App):
   
   def build(self):
       return presentation

if __name__ == "__main__":
   SimpleKivy().run()
