from kivy.config import Config
Config.set('graphics','resizable', 0) #you need to set this so the window will size based on a number input
from kivy.app import App
import time
import threading
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Line, InstructionGroup, Canvas, CanvasBase, Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.modalview import ModalView 
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock, mainthread
from pynput import mouse
from pynput.mouse import Controller
from kivy.uix.image import Image
from win32gui import GetWindowText, GetForegroundWindow, FindWindow
import win32api, win32gui
import win32con
import sys, os
#from win32gui import GetWindowText, GetForegroundWindow

mouse2 = Controller()

#Here is an example of how to properly position and size widgets to account for changes in screen resolution and resizing of the window. Please take note of the differences between the 
#minimize, maximize, window, and close buttons at the top and the other buttons. 
 
#You should always use complete pixels (not partial pixels) to size and position widgets to avoid blurryness of the widgets. The int() function can be used to convert partial pixels to complete pixels. 

Builder.load_string("""
<ButtonsApp>:
    FloatLayout:
        id: my_layout
        #//Minimize, Maximize, Window, and Close Buttons//
        #these are always positioned in the right hand corner of the window.. 
        Button:
            id: s1
            background_color: 1, 0, 0, 0
            size_hint: None, None
            size: 25, 20
            #pos: root.right - 120, root.top - 25
            #size: int(app.get_screen_width() * .01302083), int(app.get_screen_height() * .01923077)
            pos: int(root.right - (app.get_screen_width() * .0625)), int(root.top - (app.get_screen_height() * .02403846))
            opacity: 1
            Image:
                id: t1
                source: 'minimize_icon_blue.png'
                size: 23, 18
                #pos: root.right - 120, root.top - 25
                #size: int(app.get_screen_width() * .01197917), int(app.get_screen_height() * .01730769)
                pos: int(root.right - (app.get_screen_width() * .0625)), int(root.top - (app.get_screen_height() * .02403846))
        Button:
            id: s2
            background_color: 1, 0, 0, 0
            size_hint: None, None
            size: 25, 20
            #pos: root.right - 74, root.top - 25
            #size: int(app.get_screen_width() * .01302083), int(app.get_screen_height() * .01923077)
            pos: int(root.right - (app.get_screen_width() * .03854167)), int(root.top - (app.get_screen_height() * .02403846))
            opacity: 1
            Image:
                id: t2
                source: 'window_icon_blue.png'
                size: 15, 15
                #pos: root.right - 70, root.top - 23
                #size: int(app.get_screen_width() * .0078125), int(app.get_screen_height() * .01442308)
                pos: int(root.right - (app.get_screen_width() * .03645833)), int(root.top - (app.get_screen_height() * .02307692))               
        Button:
            id: s3
            background_color: 1, 0, 0, 0
            size_hint: None, None
            size: 25, 20
            #pos: root.right - 76, root.top - 25
            #size: int(app.get_screen_width() * .01302083), int(app.get_screen_height() * .01923077)
            pos: int(root.right - (app.get_screen_width() * .03958333)), int(root.top - (app.get_screen_height() * .02403846))
            opacity: 0
            Image:
                id: t3
                source: 'maximize_icon_blue.png'
                size: 12, 12
                #pos: root.right - 70, root.top - 22
                #size: int(app.get_screen_width() * .00625), int(app.get_screen_height() * .01153846)
                pos: int(root.right - (app.get_screen_width() * .03645833)), int(root.top - (app.get_screen_height() * .02115385))
        Button:
            id: s4
            background_color: 1, 0, 0, 0
            size_hint: None, None
            size: 25, 20
            #pos: root.right - 34, root.top - 25
            #size: int(app.get_screen_width() * .01302083), int(app.get_screen_height() * .01923077)
            pos: int(root.right - (app.get_screen_width() * .01770833)), int(root.top - (app.get_screen_height() * .02403846))
            opacity: 1
            Image:
                id: t4
                source: 'close_icon_blue.png'
                size: 16, 16
                #pos: root.right - 30, root.top - 24
                #size: int(app.get_screen_width() * .00833333), int(app.get_screen_height() * .01538462)
                pos: int(root.right - (app.get_screen_width() * .015625)), int(root.top - (app.get_screen_height() * .02403846))
        #//Test Labels and Buttons - Other Buttons//
        #the y portion of the position should always be calculated from the top of the window (root.top)
        Button:
            id: test_me
            text: 'test me'
            background_color: 0, 1, 0, 1
            size_hint: None, None
            #size: 1800, 100 #these raw pixel inputs for size and position will not work when the screen resolution changes from 1920/1080 to something else..
            #pos: 50, 900
            size: int(app.get_screen_width() * .9375), int(app.get_screen_height() * .09615385) #we need to adjust the size and position of the widgets to account for various screen resolutions!!
            pos: int(app.get_screen_width() * .02604167), int(root.top - (app.get_screen_height() * .20865385)) #we must calculate the y portion of the position based on a proportional distance from the top of the window
        Button:
            text: 'test me'
            background_color: 0, 0, 1, 1
            size_hint: None, None
            #size: 1800, 100
            #pos: 50, 900
            size: int(app.get_screen_width() * .9375), int(app.get_screen_height() * .09615385)
            pos: int(app.get_screen_width() * .02604167), int(root.top - (app.get_screen_height() * .40096154))
        Button:
            text: 'test me'
            background_color: 1, 0, 0, 1
            size_hint: None, None
            #size: 1800, 100
            #pos: 50, 300
            size: int(app.get_screen_width() * .9375), int(app.get_screen_height() * .09615385)
            pos: int(app.get_screen_width() * .02604167), int(root.top - (app.get_screen_height() * .68942308))
        Button:
            text: 'test me'
            background_color: 1, .5, 0, 1
            size_hint: None, None
            #size: 1800, 100
            #pos: 50, 300
            size: int(app.get_screen_width() * .9375), int(app.get_screen_height() * .09615385)
            pos: int(app.get_screen_width() * .02604167), int(root.top - (app.get_screen_height() * .97788462))

""")

class ButtonsApp(App, FloatLayout):

    def build(self):
        global icon_active
        global my_layout
        global touch_down_active
        global mouse_listener_active
        global click_listener_active
        global last_mouse_pos_x
        global last_mouse_pos_y
        global window_id
        last_mouse_pos_x = 0
        last_mouse_pos_y = 0
        mouse_listener_active = 'Y'
        click_listener_active = 'Y'
        touch_down_active = 'N'
        my_layout = self.ids.my_layout
        click_status = 'released'
        icon_active = 'window'
        Window.borderless = 1 #disable Windows title bar
        Window.left = Window.original_screen_pos_left #x position of the window 
        Window.top = Window.original_screen_pos_top #y position of the window
        Window.size = [Window.original_screen_width, Window.original_screen_height] #set the width and height of the window. Since the Windows title bar is now gone, we have to extend the height of the Kivy Window.
        Window.bind(mouse_pos=self.on_mouse_pos)
        threading.Thread(target=self.mouse_listener).start() #start the mouse_listener method in a second thread..this listener runs constantly to check if the mouse has been moved by the user..
        #window_id = FindWindow(0, 'Buttons')
        pos = (500, 500)
        window_id = win32gui.WindowFromPoint(pos) #fetch this app's window handle/id
        #print ("get window from point = " + str(window_id))

        #hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION) #this loads a default garbage looking icon from the system

        #this adds a NEW icon in the system tray (by the clock)
        #flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        #nid = (window_id, 0, flags, win32con.WM_USER+20, hicon, "Python Demo")
        #win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid) 

        #win32gui.SendMessage(window_id, win32con.WM_SETICON, win32con.ICON_SMALL, hicon) #this allows me to change the little icon on the title bar for THIS APP
        #win32gui.SendMessage(window_id, win32con.WM_SETICON, win32con.ICON_BIG, hicon) #this allows me to change the icon in the ALT+TAB screen for THIS APP

        #self.oldWndProc = win32gui.SetWindowLong(window_id, win32con.GWL_WNDPROC, self.MyWndProc)
        #self.msgdict = {} 
        #for name in dir(win32con):
            #if name.startswith("WM_"):
                #value = getattr(win32con, name)
                #self.msgdict[value] = name

        #this removes the border around the window and shows the window
        #win32gui.SetWindowLong(window_id, win32con.GWL_STYLE, 0)
        #win32gui.ShowWindow(window_id, win32con.SW_SHOW)
        return self

    #this allows us to track window events related to the kivy window using win32 API
    #def MyWndProc(self, hWnd, msg, wParam, lParam):
        #print (self.msgdict.get(msg))
        #if self.msgdict.get(msg) == 'WM_GETICON':
            #print (self.msgdict.get(msg))
        #if msg == win32con.WM_DESTROY: 
            #win32api.SetWindowLong(window_id, win32con.GWL_WNDPROC, self.oldWndProc)
        #return win32gui.CallWindowProc(self.oldWndProc, hWnd, msg, wParam, lParam)

        
    def on_mouse_pos(self, instance, pos):
        if icon_active == 'maximize':
            #here is where we control the display of various mouse cursors as the mouse hovers over edges of the window
            if pos[1] < 7 and pos[0] < Window.size[0] - 7:
                Window.set_system_cursor('size_ns') #north to south arrow for vertical sizing
            elif pos[1] < 7 and pos[0] > Window.size[0] - 7:
                Window.set_system_cursor('size_nwse') #northwest to southeast arrow for diagonal sizing
            elif pos[1] > 8 and pos[0] > Window.size[0] - 7:
                Window.set_system_cursor('size_we') #west to east arrow for horizontal sizing
            else:
                Window.set_system_cursor('arrow') #normal arrow

    def on_touch_down(self, touch):
        global start_window_height
        global start_window_width
        global start_window_top
        global start_window_left
        global start_pos_x
        global start_pos_y
        global on_touch_move_cnt
        global icon_active
        global window_resize_feature
        global touch_down_active
        global mouse_listener_active
        if touch.button == 'left': #only run all this on a left click..
            touch_down_active = 'N'
            window_resize_feature = 'disabled'
            start_window_height = Window.size[1]
            start_window_width = Window.size[0]
            start_window_top = Window.top
            start_window_left = Window.left
            start_pos_x = mouse2.position[0]
            start_pos_y = mouse2.position[1]
            #//Minimize Button Clicked//
            if self.ids.s1.collide_point(touch.pos[0], touch.pos[1]):
                Window.last_screen_pos_left = Window.left
                Window.last_screen_pos_top = Window.top
                Window.disable_on_restore = 'N'
                Window.minimize()
                Clock.schedule_interval(self.maximize_listener, .1) #kick off the maximize listener to wait for the user to click the python icon in the Windows task bar..
            #//Window Button Clicked//
            if icon_active == 'window':
                if self.ids.s2.collide_point(touch.pos[0], touch.pos[1]):
                    Window.disable_on_restore = 'N'
                    Window.last_screen_width = Window.original_screen_width / 2
                    Window.last_screen_height = Window.original_screen_height / 2
                    Window.on_restore()
                    on_touch_move_cnt = 1
                    self.ids.s2.opacity = 0
                    self.ids.s3.opacity = 1
                    icon_active = 'maximize'
                    touch_down_active = 'N'
            #//Maximize Button Clicked//
            if icon_active == 'maximize':
                if self.ids.s3.collide_point(touch.pos[0], touch.pos[1]): 
                    Window.disable_on_restore = 'N'
                    #find which monitor the window is currently using window left and top position - look in taskbar included position coordinates
                    i = 0
                    for row in Window.monitor_data_incl_taskbar:
                        if Window.left >= row[0] and Window.left < row[1] and Window.top >= row[2] and Window.top < row[3]:
                            break #stop the loop and use i below
                        i = i + 1
                    #update window position and size
                    Window.last_screen_pos_left = Window.monitor_data_excl_taskbar[i][0]
                    Window.last_screen_pos_top = Window.monitor_data_excl_taskbar[i][2]
                    Window.last_screen_width = Window.monitor_data_excl_taskbar[i][4]
                    Window.last_screen_height = Window.monitor_data_excl_taskbar[i][5]
                    Window.on_restore()
                    self.ids.s2.opacity = 1
                    self.ids.s3.opacity = 0
                    icon_active = 'window'
            #//Close Button Clicked//
            if self.ids.s4.collide_point(touch.pos[0], touch.pos[1]): #if close button is clicked..
                mouse_listener_active = 'N'
                click_listener_active = 'N'
                Window.close()
            #//Window Resize Feature Activated//
            if icon_active == 'maximize':
                #here is where we determine which window drag feature the user is trying to utilize
                if touch.pos[1] < 7 and touch.pos[0] < Window.size[0] - 7:
                    window_resize_feature = 'n_s' #north to south arrow for vertical sizing
                elif touch.pos[1] < 7 and touch.pos[0] > Window.size[0] - 7:
                    window_resize_feature = 'nw_se' #northwest to southeast arrow for diagonal sizing
                elif touch.pos[1] > 8 and touch.pos[0] > Window.size[0] - 7:
                    window_resize_feature = 'w_e' #west to east arrow for horizontal sizing
                else:
                    window_resize_feature = 'disabled'
            touch_down_active = 'Y'

    #We have to run this special listener to account for when the user clicks the minimize button in the App and then clicks the App icon in the Window's task bar to restore the Window..
    def maximize_listener(self, *args):
        global icon_active
        #once the user minimizes the window, we will initiate this listener to run and to check for the maximize_trigger variable within the Window source code to update.
        #once the listener notices that the variable has been updated by the user clicking the icon in the Window's task bar, the window will restore and we will update the maximize icon and disable the listener..
        if Window.maximize_trigger == 'Y':
            Window.disable_on_restore = 'Y'
            Window.on_restore()
            #if the screen was originally not in a maximized view before minimize was clicked then..
            if Window.last_screen_width < Window.original_screen_width or Window.last_screen_height < Window.original_screen_height: 
                self.ids.s2.opacity = 0
                self.ids.s3.opacity = 1
                icon_active = 'maximize'
            else:
                self.ids.s2.opacity = 1
                self.ids.s3.opacity = 0
                icon_active = 'window'
            Window.maximize_trigger = 'N' #reset the trigger variable back to N
            Clock.unschedule(self.maximize_listener) #unschedule the listener as it is no longer needed

    #pynput mouse release tracking - we use this so we can track release of the mouse whether the mouse is in the kivy window or not.. It works better than kivy's on_touch_up in this case.. 
    def on_click(x, y, button, pressed):
        global click_listener_active
        global touch_down_active
        global window_id
        if not pressed: #if mouse is released..
            touch_down_active = 'N'
        if click_listener_active == 'N':
            return False

    #this is the pynput listener tracking the release of the mouse
    listener = mouse.Listener(on_click=on_click)
    listener.start()

    def mouse_listener(self): #this is running constantly in another thread while the Kivy App is running..
        global last_mouse_pos_x
        global last_mouse_pos_y
        global mouse_listener_active
        global touch_down_active
        global window_resize_feature
        while mouse_listener_active == 'Y':
            if mouse2.position[0] != last_mouse_pos_x or mouse2.position[1] != last_mouse_pos_y:
                last_mouse_pos_x = mouse2.position[0]
                last_mouse_pos_y = mouse2.position[1]
                if touch_down_active == 'Y':
                    if window_resize_feature == 'disabled':
                        Clock.schedule_once(self.move_window) #this will move the window as the user drags the mouse cursor around after a left click..
                    else:
                        Clock.schedule_once(self.size_window)

    def move_window(self, *args):
        global start_pos_x
        global start_pos_y
        global last_mouse_pos_x
        global last_mouse_pos_y
        global start_window_left
        global start_window_top
        Window.left = start_window_left + (last_mouse_pos_x - start_pos_x)
        Window.top = start_window_top + (last_mouse_pos_y - start_pos_y)
        Window.last_screen_pos_left = Window.left
        Window.last_screen_pos_top = Window.top
        Clock.unschedule(self.move_window)

    def size_window(self, *args):
        global start_pos_x
        global start_pos_y
        global last_mouse_pos_x
        global last_mouse_pos_y
        global start_window_height
        global start_window_width
        global window_resize_feature
        if window_resize_feature == 'n_s':
            Window.disable_on_restore = 'Y'
            Window.size = [start_window_width, start_window_height + (last_mouse_pos_y - start_pos_y)]
        if window_resize_feature == 'nw_se':
            Window.disable_on_restore = 'Y'
            Window.size = [start_window_width + (last_mouse_pos_x - start_pos_x), start_window_height + (last_mouse_pos_y - start_pos_y)]
        if window_resize_feature == 'w_e':
            Window.disable_on_restore = 'Y'
            Window.size = [start_window_width + (last_mouse_pos_x - start_pos_x), start_window_height]
        Window.last_screen_width = Window.size[0]
        Window.last_screen_height = Window.size[1]
        Window.disable_on_restore = 'N'
        Clock.unschedule(self.size_window)

    def get_screen_width(self):
        screen_width = Window.monitor_data_excl_taskbar[0][4]
        return screen_width

    def get_screen_height(self):
        screen_height = Window.monitor_data_excl_taskbar[0][5]
        return screen_height

if __name__ == "__main__":
    ButtonsApp().run()


