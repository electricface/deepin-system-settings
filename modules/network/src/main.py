#!/usr/bin/env python
#-*- coding:utf-8 -*-
import dss
import dbus
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default = True)
dbus.mainloop.glib.threads_init()
import sys
import os
from deepin_utils.file import  get_parent_dir
from deepin_utils.ipc import is_dbus_name_exists
sys.path.append(os.path.join(get_parent_dir(__file__, 4), "dss"))
from module_frame import ModuleFrame 
from helper import Dispatcher

from nm_modules import nm_module
from main_ui import Network
from nls import _
from dss_log import log

slider = nm_module.slider

def start_ui(network):
    print "start ui"
    network.refresh()

if __name__ == '__main__':
    module_frame = ModuleFrame(os.path.join(get_parent_dir(__file__, 2), "config.ini"))
    Dispatcher.load_module_frame(module_frame)
    Dispatcher.load_slider(slider)

    module_frame.add(slider)

    if is_dbus_name_exists("org.freedesktop.NetworkManager", False):
        n = Network()
        Dispatcher.connect("service-start-do-more", lambda w: start_ui(n))
        
        def message_handler(*message):
            (message_type, message_content) = message
            if message_type == "show_again":
                slider._set_to_page("main")
                module_frame.send_module_info()
            elif message_type == "click_crumb":
                print "click_crumb"
                (crumb_index, crumb_label) = message_content
                if crumb_index == 1:
                    slider._slide_to_page("main", "none")
                if crumb_label == _("VPN"):
                    slider._slide_to_page("vpn", "none")

        module_frame.module_message_handler = message_handler
        module_frame.run()
