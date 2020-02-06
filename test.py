from kivy.config import Config
Config.set('graphics','resizable', 0) #you need to set this so the window will size based on a number input
from kivy.app import App
import time
import threading
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from pynput import mouse
from pynput.mouse import Controller
from kivy.uix.image import Image
import uiautomation 
from uiautomation import GetElementFromPoint, GetParentElement, GetElementInfo #these are newly added methods to make this example work
import win32api, win32gui
import win32con
import win32com.client
from win32gui import SetForegroundWindow
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.button import Button

mouse2 = Controller()
shell = win32com.client.Dispatch("WScript.Shell")

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
            pos: int(root.right - (app.get_screen_width() * .0625)), int(root.top - (app.get_screen_height() * .02403846))
            opacity: 1
            Image:
                id: t1
                source: 'minimize_icon_blue.png'
                size: 23, 18
                pos: int(root.right - (app.get_screen_width() * .0625)), int(root.top - (app.get_screen_height() * .02403846))
        Button:
            id: s2
            background_color: 1, 0, 0, 0
            size_hint: None, None
            size: 25, 20
            pos: int(root.right - (app.get_screen_width() * .03854167)), int(root.top - (app.get_screen_height() * .02403846))
            opacity: 1
            Image:
                id: t2
                source: 'window_icon_blue.png'
                size: 15, 15
                pos: int(root.right - (app.get_screen_width() * .03645833)), int(root.top - (app.get_screen_height() * .02307692))               
        Button:
            id: s3
            background_color: 1, 0, 0, 0
            size_hint: None, None
            size: 25, 20
            pos: int(root.right - (app.get_screen_width() * .01770833)), int(root.top - (app.get_screen_height() * .02403846))
            opacity: 1
            Image:
                id: t3
                source: 'close_icon_blue.png'
                size: 16, 16
                pos: int(root.right - (app.get_screen_width() * .015625)), int(root.top - (app.get_screen_height() * .02403846))
        #//Test Labels and Buttons - Other Buttons//
        #the y portion of the position should always be calculated from the top of the window (root.top)
        Button:
            id: test_me
            text: 'test me'
            background_color: 0, 1, 0, 1
            size_hint: None, None
            size: int(app.get_screen_width() * .9375), int(app.get_screen_height() * .09615385) #we need to adjust the size and position of the widgets to account for various screen resolutions!!
            pos: int(app.get_screen_width() * .02604167), int(root.top - (app.get_screen_height() * .20865385)) #we must calculate the y portion of the position based on a proportional distance from the top of the window
        Button:
            text: 'test me'
            background_color: 0, 0, 1, 1
            size_hint: None, None
            size: int(app.get_screen_width() * .9375), int(app.get_screen_height() * .09615385)
            pos: int(app.get_screen_width() * .02604167), int(root.top - (app.get_screen_height() * .40096154))
        Button:
            text: 'test me'
            background_color: 1, 0, 0, 1
            size_hint: None, None
            size: int(app.get_screen_width() * .9375), int(app.get_screen_height() * .09615385)
            pos: int(app.get_screen_width() * .02604167), int(root.top - (app.get_screen_height() * .68942308))
        Button:
            text: 'test me'
            background_color: 1, .5, 0, 1
            size_hint: None, None
            size: int(app.get_screen_width() * .9375), int(app.get_screen_height() * .09615385)
            pos: int(app.get_screen_width() * .02604167), int(root.top - (app.get_screen_height() * .97788462))

""")

class ButtonsApp(App, FloatLayout):

    def get_window_id():
        pos = (500, 500)
        return win32gui.WindowFromPoint(pos)

    click_listener_active = 'Y'
    window_move_active = 'N' 
    window_resize_active = 'N'
    window_id = get_window_id()

    def build(self):
        global s2
        global t2
        global icon_active
        global mouse_listener_active
        global last_mouse_pos_x
        global last_mouse_pos_y
        global touch_down_active
        pos = (500, 500)
        ButtonsApp.window_id = win32gui.WindowFromPoint(pos)
        s2 = self.ids.s2
        t2 = self.ids.t2
        icon_active = 'window'
        Window.window_state = 'open'
        last_mouse_pos_x = 0
        last_mouse_pos_y = 0
        mouse_listener_active = 'Y'
        touch_down_active = 'N'
        Window.borderless = 1 #disable Windows title bar
        Window.left = Window.original_screen_pos_left #x position of the window 
        Window.top = Window.original_screen_pos_top #y position of the window
        Window.size = [Window.original_screen_width, Window.original_screen_height] #set the width and height of the window. Since the Windows title bar is now gone, we have to extend the height of the Kivy Window.
        Window.bind(mouse_pos=self.on_mouse_pos)
        Window.bind(on_request_close=self.on_request_close)
        threading.Thread(target=self.mouse_listener).start() #start the mouse_listener method in a second thread..this listener runs constantly to check if the mouse has been moved by the user..
        return self

    def on_mouse_pos(self, instance, pos):
        Window.set_system_cursor('arrow') #normal arrow
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
        if touch.button == 'left': #only run all this on a left click..
            global touch_down_active
            global mouse_listener_active
            global last_mouse_pos_x
            global last_mouse_pos_y
            global start_window_height
            global start_window_width
            global start_window_top
            global start_window_left
            global start_pos_x
            global start_pos_y
            global window_resize_feature
            global window_move_resize_active
            global icon_active
            touch_down_active = 'N'
            window_move_resize_active = 'Y'
            window_resize_feature = 'disabled'
            start_window_height = Window.size[1]
            start_window_width = Window.size[0]
            start_window_top = Window.top
            start_window_left = Window.left
            start_pos_x = mouse2.position[0]
            start_pos_y = mouse2.position[1]
            if touch.pos[1] > Window.size[1] - (Window.size[1] * .01923077): #this will limit dragging of the window to only when the cursor is near the very TOP of the window..
                ButtonsApp.window_move_active = 'Y'
            else:
                ButtonsApp.window_move_active = 'N'
            #//Minimize Button Clicked//
            if self.ids.s1.collide_point(touch.pos[0], touch.pos[1]):
                threading.Thread(target=self.disable_window_move_resize).start()
                Window.last_screen_pos_left = Window.left
                Window.last_screen_pos_top = Window.top
                Window.minimize()
                Window.window_state = 'minimized'
            if self.ids.s2.collide_point(touch.pos[0], touch.pos[1]):
                #//Window Button Clicked//
                if icon_active == 'window':
                    threading.Thread(target=self.disable_window_move_resize).start()
                    Window.disable_on_restore = 'N'
                    Window.last_screen_width = Window.original_screen_width / 2
                    Window.last_screen_height = Window.original_screen_height / 2
                    Window.on_restore()
                    #change the button to a maximize button..
                    self.ids.s2.size = [25, 20]
                    self.ids.s2.pos = [int(Window.size[0] - (self.get_screen_width() * .03958333)), int(Window.size[1] - (self.get_screen_height() * .02403846))]
                    self.ids.t2.size = [12, 12]
                    self.ids.t2.pos = [int(Window.size[0] - (self.get_screen_width() * .03645833)), int(Window.size[1] - (self.get_screen_height() * .02115385))]
                    self.ids.t2.source = 'maximize_icon_blue.png'
                    touch_down_active = 'N'
                    icon_active = 'maximize'
                #//Maximize Button Clicked//
                elif icon_active == 'maximize':
                    threading.Thread(target=self.disable_window_move_resize).start()
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
                    #change the button to a window button..
                    self.ids.s2.size = [25, 20]
                    self.ids.s2.pos = [int(Window.size[0] - (self.get_screen_width() * .03854167)), int(Window.size[1] - (self.get_screen_height() * .02403846))]
                    self.ids.t2.size = [15, 15]
                    self.ids.t2.pos = [int(Window.size[0] - (self.get_screen_width() * .03645833)), int(Window.size[1] - (self.get_screen_height() * .02307692))]
                    self.ids.t2.source = 'window_icon_blue.png'
                    icon_active = 'window'
            #//Close Button Clicked//
            if self.ids.s3.collide_point(touch.pos[0], touch.pos[1]): #if close button is clicked..
                mouse_listener_active = 'N'
                ButtonsApp.click_listener_active = 'N'
                Window.close()
            #//Window Resize Feature Activated//
            if icon_active == 'maximize':
                #here is where we determine which window drag feature the user is trying to utilize
                if touch.pos[1] < 7 and touch.pos[0] < Window.size[0] - 7:
                    window_resize_feature = 'n_s' #north to south arrow for vertical sizing
                    ButtonsApp.window_resize_active = 'Y'
                elif touch.pos[1] < 7 and touch.pos[0] > Window.size[0] - 7:
                    window_resize_feature = 'nw_se' #northwest to southeast arrow for diagonal sizing
                    ButtonsApp.window_resize_active = 'Y'
                elif touch.pos[1] > 8 and touch.pos[0] > Window.size[0] - 7:
                    window_resize_feature = 'w_e' #west to east arrow for horizontal sizing
                    ButtonsApp.window_resize_active = 'Y'
                else:
                    window_resize_feature = 'disabled'
            touch_down_active = 'Y'

    #pynput mouse tracking
    def on_click(x, y, button, pressed):
        global touch_down_active
        global window_move_resize_active
        if pressed: 
            Clock.schedule_once(ButtonsApp.get_control_info)
        if not pressed: #if mouse is released..
            window_move_resize_active = 'N'
            ButtonsApp.window_resize_active = 'N'
            ButtonsApp.window_move_active = 'N'
            touch_down_active = 'N'
        if ButtonsApp.click_listener_active == 'N':
            return False

    #this is the pynput listener tracking the release of the mouse
    listener = mouse.Listener(on_click=on_click)
    listener.start()

    def mouse_listener(self): #this is running constantly in another thread while the Kivy App is running..
        global mouse_listener_active
        global last_mouse_pos_x
        global last_mouse_pos_y
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
        global last_mouse_pos_x
        global last_mouse_pos_y
        global start_window_left
        global start_window_top
        global start_pos_x
        global start_pos_y
        if window_move_resize_active == 'Y' and ButtonsApp.window_move_active == 'Y':
            Window.left = start_window_left + (last_mouse_pos_x - start_pos_x)
            Window.top = start_window_top + (last_mouse_pos_y - start_pos_y)
            Window.last_screen_pos_left = Window.left
            Window.last_screen_pos_top = Window.top
            Clock.unschedule(self.move_window)

    def size_window(self, *args):
        global window_move_resize_active
        global window_resize_feature
        global start_window_width
        global start_window_height
        global last_mouse_pos_x
        global last_mouse_pos_y
        global start_pos_y
        global start_pos_x
        if window_move_resize_active == 'Y' and ButtonsApp.window_resize_active == 'Y':
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

    def get_control_info(self):
        global element_clicked
        try: 
            #analyze the ControlType and Automation ID of the element that was clicked..
            element_clicked = uiautomation.GetElementFromPoint(mouse2.position[0], mouse2.position[1]) #returns the element that you clicked (this has to run here or it errors)
            element_clicked_info = GetElementInfo(element_clicked) #returns info about the element you clicked
            ctp = str(element_clicked_info).find('ControlType:')
            cnp = str(element_clicked_info).find('ClassName:')
            ct = str(element_clicked_info)[ctp + 13:cnp - 1]
            ct = ct[0:ct.find(' ')]
            aip = str(element_clicked_info).find('AutomationId:')
            rp = str(element_clicked_info).find('Rect:')
            aid = str(element_clicked_info)[aip + 13:rp - 1]
            if 'python.exe' in str(aid) and str(ct) == 'ButtonControl': #We have to look for 'python.exe' as a UIAutomation ID when the app icon in the taskbar is clicked.. not very elegant but it works..
                #analyze the classname of the parent element.. we are looking to see if it is a taskbar classname
                parent_of_element_clicked = uiautomation.GetParentElement(element_clicked) #returns the parent of the element that you clicked
                parent_of_element_clicked_info = GetElementInfo(parent_of_element_clicked) #returns info about the parent of the element you clicked
                cnp = str(parent_of_element_clicked_info).find('ClassName:')
                aip = str(parent_of_element_clicked_info).find('AutomationId:')
                cn = str(parent_of_element_clicked_info)[cnp + 11:aip - 1]
                cn = cn[0:cn.find(' ')]
                if cn == 'MSTaskListWClass': #this is the taskbar classname
                    if Window.window_state == 'open':
                        Window.last_screen_pos_left = Window.left
                        Window.last_screen_pos_top = Window.top
                        Window.last_screen_width = Window.width
                        Window.last_screen_height = Window.height
                        Clock.schedule_once(ButtonsApp.minimize_window)
                    else:
                        Clock.schedule_once(ButtonsApp.re_open_window)
            if 'python.exe' not in str(aid) and str(ct) == 'ButtonControl':
                #analyze the classname of the parent element.. we are looking to see if it is a taskbar classname
                parent_of_element_clicked = uiautomation.GetParentElement(element_clicked) #returns the parent of the element that you clicked
                parent_of_element_clicked_info = GetElementInfo(parent_of_element_clicked) #returns info about the parent of the element you clicked
                cnp = str(parent_of_element_clicked_info).find('ClassName:')
                aip = str(parent_of_element_clicked_info).find('AutomationId:')
                cn = str(parent_of_element_clicked_info)[cnp + 11:aip - 1]
                cn = cn[0:cn.find(' ')]
                if cn == 'MSTaskListWClass':
                    Window.window_state = 'minimized'
        except:
            pass
        Clock.unschedule(ButtonsApp.get_control_info)

    def minimize_window(self):
        Window.disable_on_restore = 'Y'
        Window.minimize()
        Window.window_state = 'minimized'
        Clock.unschedule(ButtonsApp.minimize_window)

    def re_open_window(self):
        global s2
        global s3
        global icon_active
        Window.disable_on_restore = 'N'
        Window.on_restore()
        shell.SendKeys('%') #you MUST run this or the SetForegroundWindow code will error!!
        win32gui.SetForegroundWindow(ButtonsApp.window_id)
        Window.window_state = 'open'
        if Window.last_screen_width < Window.original_screen_width or Window.last_screen_height < Window.original_screen_height: 
            icon_active = 'maximize'
        else:
            icon_active = 'window'
        Window.set_system_cursor('arrow') #normal arrow
        Clock.unschedule(ButtonsApp.re_open_window)

    def on_request_close(self, *args):
        global mouse_listener_active
        mouse_listener_active = 'N'
        ButtonsApp.click_listener_active = 'N'

    def disable_window_move_resize(self): #temporarily disable window move and resize..
        global window_move_resize_active
        global icon_active
        window_move_resize_active = 'N'
        ButtonsApp.window_resize_active = 'N'
        ButtonsApp.window_move_active = 'N'
        time.sleep(2)
        window_move_resize_active = 'Y'
        ButtonsApp.window_resize_active = 'Y'
        ButtonsApp.window_move_active = 'Y'

    def get_screen_width(self):
        screen_width = Window.monitor_data_excl_taskbar[0][4]
        return screen_width

    def get_screen_height(self):
        screen_height = Window.monitor_data_excl_taskbar[0][5]
        return screen_height

if __name__ == "__main__":
    ButtonsApp().run()


