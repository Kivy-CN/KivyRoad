# Kivy-simple-tutorial
___

几个月不写中文了， 感觉还行。 So, let's begin our journey.
___

首先，有两个网址你不得不看：

1. [Kivy: Cross-platform Python Framework for NUI](https://kivy.org/#home)
在官网逛逛，顺便看看最下面的代码，try to run it.

2. [https://www.youtube.com/playlist?list=PLQVvvaa0QuDe_l6XiJ40yGTEqIKugAdTy](https://www.youtube.com/playlist?list=PLQVvvaa0QuDe_l6XiJ40yGTEqIKugAdTy)
sentdex大神的入门级教程。
___

Kivy总体思想是：kv代码管界面，python代码管逻辑。

然后重点来了， 我主要讲三件事：(kv访问Python；Python访问kv；窗口)。
___

## 一阶段：

#### 1.Python访问kv

Python可以直接调用kv代码。如：
```
from kivy.app import App
from kivy.lang import Builder

kv = Builder.load_string('''
Button:
    text: "I was created by kv codes"
''')

class TestApp(App):
    def build(self):
        return kv

TestApp().run()
```
#### 2.窗口

kv代码中被`<>`包裹住的是某个class的名字，这个class需在python代码中声明，它们代表同一个class。
```
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string('''
<OneScreen>
    Label:
        text: "My mother screen was created by kv and python codes."
''')

class OneScreen(Screen):
    pass

class TestApp(App):
    def build(self):
        return OneScreen()

TestApp().run()
```
#### 3. kv访问Python

在.kv文件或kv代码里，`root`只代表其上层被`<>`包裹住的类。如：
```
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string('''
<OneScreen>
    Button:
        text: 'Click me'
        on_release: print(root.__class__)
''')

class OneScreen(Screen):
    pass

class TestApp(App):
    def build(self):
        return OneScreen()

TestApp().run()
```
___

## 二阶段：

#### 1. kv访问Python
```
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string('''
<OneScreen>
    BoxLayout:
        Button:
            text: 'Click me'
            on_release: root.do_something()
        Button:
            text: 'Who made this?'
            on_release: print(root.author)
''')

class OneScreen(Screen):
    def __init__(self, **kwargs):
        self.author = 'yingshaoxo'
        super(OneScreen, self).__init__(**kwargs)
        
    def do_something(self):
        print('2333')

class TestApp(App):
    def build(self):
        return OneScreen()

TestApp().run()
```
#### 2. Python访问kv

你需要给kv组件一个id，用以标明其唯一性。再使用ids方法调用它。如：
```
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string('''
<OneScreen>
    BoxLayout:
        Button:
            id: one_ask
            text: 'Who made this?'
            on_release: root.do_something()
''')

class OneScreen(Screen):
    def __init__(self, **kwargs):
        self.author = 'yingshaoxo'
        super(OneScreen, self).__init__(**kwargs)
        
    def do_something(self):
        self.ids['one_ask'].text = self.author

class TestApp(App):
    def build(self):
        return OneScreen()

TestApp().run()
```
#### 3. 窗口

As far as I see，在做程序的时候，你会遇到很多窗口。所以`ScreenManager`这时候派上用场了。
```
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

Builder.load_string('''
<ScreenManager>:
    Screen:
        name: 'home'
        Button:
            text: 'Go to another screen'
            on_release: root.current = 'another'
            
    Screen:
        name: 'another'
        Button:
            text: "Go back home"
            on_release: root.current = 'home'
''')

class ScreenManager(ScreenManager):
    pass

class TestApp(App):
    def build(self):
        return ScreenManager()

TestApp().run()
```
___

## 三阶段：

#### 1+2. 窗口、kv访问Python

In fact, 你可以把`ScreenManager`看成一个很大的`widget`。

但如果所有的数据操作(`root.function`)都在一个 `ScreenManager` class里做的话显然不科学。

所以我们最好把每个窗口都在Python里声明一个class，这样既可以有程序启动时的总操作，又可以有各个子窗口的分操作。看示例：
```
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string('''
<ScreenManager>:
    HomeScreen
    AnotherScreen

<HomeScreen>:
    name: 'home'
    Button:
        text: 'Go to another screen'
        on_release: root.manager.current = 'another'

<AnotherScreen>:
    name: 'another'
    Button:
        text: "Go back home"
        on_release: root.manager.current = 'home'
''')

class ScreenManager(ScreenManager):
    pass

class HomeScreen(Screen):
    pass

class AnotherScreen(Screen):
    pass

class TestApp(App):
    def build(self):
        return ScreenManager()

TestApp().run()
```
我们可以看到示例不光在kv代码中绑定了两个`Screen`class，还引用了一个`root.manager `。没错，那是从`screen` class得到`screenmanager` class的方法。
#### 3. Python访问kv

直接用kv代码预先定义控件(如按钮)的行为有时不能满足我们的需求，于是我们可能需要临时改变按钮的行为：
```
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from time import gmtime, strftime # this equls cv codes #...

Builder.load_string("""
#:import gmtime time.gmtime
#:import strftime time.strftime

<RootWidget>
    BoxLayout:
        orientation: 'vertical'
        Button:
            id: change_itself
            text: 'I can change myself'
            on_release: root.ids['change_itself'].text = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
        Button:
            id: change_all
            text: 'I can change our behavior'
            on_release: root.change_all()
""")

class RootWidget(Screen):
    def change_all(self):
        print(self.ids)
        for instance_class in self.ids.values():
            instance_class.text = 'Exit'
            instance_class.bind(on_release=exit)

class TestApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    TestApp().run()
```
___

## 四阶段：Show time!
还想什么呢？赶紧动手写程序吧~
___

For more information, you can go and see:
https://kivy.org/docs/api-kivy.uix.screenmanager.html
