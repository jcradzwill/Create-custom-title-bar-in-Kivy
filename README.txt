------------High Level Overview------------

github link: https://github.com/jcradzwill/Create-custom-title-bar-in-Kivy

As of 1/28/2020, the base Kivy framework does not naturally support custom title bar features without the implementation of special workaround code. This workaround example will show you how to remove the Windows title bar and replace it with a custom title bar with minimize, window, maximize, close, window dragging, and window resizing features. The custom title bar will contain buttons for minimize, maximize, window, and close in the top right corner of the App. 

Please note that this workaround example will ONLY work on Windows OS since it involves Windows API code modifications. It was built and tested on a PC using Windows 10 OS. If you want to make this work on Mac OS,
you will need to implement similar code using the Mac OS APIs. 

This example utilizes pynput for the Window dragging and resize functionality. You can easily install pynput using pip. We use pynput instead of Kivy's on_touch_move method because it prevents the window from 'skipping'
around when it is dragged and resized as this is very annoying and not user friendly. 

This example also utilizes UI Automation. You can easily install uiautomation using pip. We use UI Automation to get around a bug in the Kivy source code that prevents the App from minimizing/maximizing when the app icon is clicked
in the taskbar while Window.borderless is set to 1. I have made a post about this bug on github here: https://github.com/kivy/kivy/issues/6707 and on stackoverflow here: https://stackoverflow.com/questions/59910143/cant-minimize-kivy-window-when-borderless-1-border-disabled

It would be really nice to get this bug fixed because it is very difficult to find and execute OS API functions that monitor clicks on app icons in the taskbar!

------------github file Overview------------

Please see below for an overview of each of the files uploaded to github to support this example:

1) __init__.py - The Window Kivy Source code file that has been modified to make this custom title bar example work. You can find this file locally on your machine here: Python37-32\Lib\site-packages\kivy\core\window\__init__.py. All code changes to this file are marked with a comment tag of #NEW CODE HERE within the file. I have specific instructions on how to modify this file in the steps below. However, it would be much easier for you to simply replace YOUR existing Kivy source code file with this one. I would recommend backing up the existing file before replacing it with this one just to be safe. 

2) test.py - This is the custom title bar test app that should run properly once you implement the code changes to the Kivy source file mentioned above. It should launch an App that has minimize, maximize, window, and close buttons in the top right corner that are clickable. You should also be able to move the App window around and resize it on the edges. 

3) close_icon_blue.png, maximize_icon_blue.png, minimize_icon_blue.png, and window_icon_blue.png - These are the png images being used for the minimize, maximize, window, and close buttons in the top right corner of the test App. Make sure you place these files in the same folder as the test.py file when you run it.

------------Kivy Window Source Code File Modification Steps------------

Please note that these Kivy Source code changes and this example will ONLY work on Windows OS since it involves Windows API code additions.

The first set of steps below involve updating the Window Kivy Source code located here: Python37-32\Lib\site-packages\kivy\core\window\__init__.py. You can open the Window Kivy source code file using an IDE to modify the code.

1) Within the Window Kivy Source code file, there are import statements at the top. Insert these new import statements (see where it says NEW CODE HERE):

from os.path import join, exists
from os import getcwd

from kivy.core import core_select_lib
from kivy.clock import Clock
from kivy.config import Config
from kivy.logger import Logger
from kivy.base import EventLoop, stopTouchApp
from kivy.modules import Modules
from kivy.event import EventDispatcher
from kivy.properties import ListProperty, ObjectProperty, AliasProperty, \
    NumericProperty, OptionProperty, StringProperty, BooleanProperty
from kivy.utils import platform, reify, deprecated
from kivy.context import get_current_context
from kivy.uix.behaviors import FocusBehavior
from kivy.setupconfig import USE_SDL2
from kivy.graphics.transformation import Matrix
from kivy.graphics.cgl import cgl_get_backend_name
from win32api import GetMonitorInfo #NEW CODE HERE - NOTE: THIS CODE WILL ONLY WORK IN WINDOWS SINCE IT USES WINDOWS API FUNCTIONS
import win32api #NEW CODE HERE
 
2) Within the WindowBase class, we need to create and populate some new variables. Basically, these variables are being used to capture screen position and screen size of all active monitors with and without taskbars. 

class WindowBase(EventDispatcher):

    #NEW CODE HERE - NOTE: THIS CODE WILL ONLY WORK IN WINDOWS SINCE IT USES WINDOWS API FUNCTIONS
    monitors = win32api.EnumDisplayMonitors() #fetch all of the monitor handles..
    monitor_data_excl_taskbar = []
    monitor_data_incl_taskbar = []
    for x in range(0, len(monitors)): #loop through the monitors and store data about them..
        #store all monitor data EXCLUDING the taskbars..
        monitor_info = GetMonitorInfo(monitors[x][0]).get("Work") 
        x1_pos = monitor_info[0]
        x2_pos = monitor_info[2]
        y1_pos = monitor_info[1]
        y2_pos = monitor_info[3]
        screen_width = x2_pos - x1_pos
        screen_height = y2_pos - y1_pos
        monitor_data_excl_taskbar.append([x1_pos, x2_pos, y1_pos, y2_pos, screen_width, screen_height])
        #store all monitor data INCLUDING the taskbars..
        monitor_info = GetMonitorInfo(monitors[x][0]).get("Monitor")
        x1_pos = monitor_info[0]
        x2_pos = monitor_info[2]
        y1_pos = monitor_info[1]
        y2_pos = monitor_info[3]
        screen_width = x2_pos - x1_pos
        screen_height = y2_pos - y1_pos
        monitor_data_incl_taskbar.append([x1_pos, x2_pos, y1_pos, y2_pos, screen_width, screen_height])
    disable_on_restore = 'N'
    maximize_trigger = 'N'
    original_screen_pos_left = monitor_data_excl_taskbar[0][0] #get the x position of the primary screen's resolution excluding taskbars
    original_screen_pos_top = monitor_data_excl_taskbar[0][2] #get the y position of the primary screen's resolution excluding taskbars
    original_screen_width = monitor_data_excl_taskbar[0][4] #get the width of the primary screen's resolution excluding taskbars
    original_screen_height = monitor_data_excl_taskbar[0][5] #get the height of the primary screen's resolution excluding taskbars
    last_screen_pos_left = original_screen_pos_left
    last_screen_pos_top = original_screen_pos_top
    last_screen_width = original_screen_width 
    last_screen_height = original_screen_height

    '''WindowBase is an abstract window widget for any window implementation.

3) Locate the 'def on_restore' method and modify it to the following:

    def on_restore(self, *largs):
        '''Event called when the window is restored.

        .. versionadded:: 1.10.0

        .. note::
            This feature requires the SDL2 window provider.
       
        '''
        #NEW CODE HERE
        if Window.disable_on_restore == 'N': #we have to disable this on_restore event from running when the app size is reduced using    windowed button
            Window.left = Window.last_screen_pos_left
	    Window.top = Window.last_screen_pos_top
            Window.size = [Window.last_screen_width, Window.last_screen_height]
        pass

------------Running the Test App------------

Once you have completed the Kivy Source code modifications mentioned above, you should be able to run the test App (test.py file) with no problems. 

Locate the example test.py file, run it, and see what it does. Within this test app, there are specific methods that are called to account for the user minimizing, maximizing, windowing, and closing the window using the buttons at the top and clicking the python icon in the taskbar. You should also be able to 'window' the app, move it around, and resize it.

Within the test app's code, you will notice that we utilize the newly created variables that we created in the source code modification steps above. Since the native Windows title bar is gone, we must account for all aspects of the user manipulating the window using python: minimize, maximize, window, close, window dragging, and window resizing.
