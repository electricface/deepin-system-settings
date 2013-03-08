#! /usr/bin/env python                                                          
# -*- coding: utf-8 -*-                                                         
                                                                                
# Copyright (C) 2013 Deepin, Inc.                                        
#               2013 Zhai Xiang                                          
#                                                                               
# Author:     Zhai Xiang <zhaixiang@linuxdeepin.com>                            
# Maintainer: Zhai Xiang <zhaixiang@linuxdeepin.com>                            
#                                                                               
# This program is free software: you can redistribute it and/or modify          
# it under the terms of the GNU General Public License as published by          
# the Free Software Foundation, either version 3 of the License, or             
# any later version.                                                            
#                                                                               
# This program is distributed in the hope that it will be useful,               
# but WITHOUT ANY WARRANTY; without even the implied warranty of                
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 
# GNU General Public License for more details.                                  
#                                                                               
# You should have received a copy of the GNU General Public License             
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys                                                                      
import os                                                                       
from deepin_utils.file import get_parent_dir                                    
sys.path.append(os.path.join(get_parent_dir(__file__, 4), "dss"))

from theme import app_theme
from dtk.ui.draw import draw_text
from dtk.ui.box import ImageBox
from dtk.ui.label import Label
from dtk.ui.constant import ALIGN_START, ALIGN_MIDDLE, ALIGN_END
from dtk.ui.button import ToggleButton
from dtk.ui.line import HSeparator
from dtk.ui.new_treeview import TreeItem, TreeView
from vtk.button import SelectButton
from deepin_utils.process import run_command
import gobject
import gtk
import pango
import time
from my_bluetooth import MyBluetooth
from nls import _

class DeviceItem(TreeItem):
    ITEM_HEIGHT = 15
    NAME_WIDTH = 160
    
    def __init__(self, name):
        TreeItem.__init__(self)
        self.name = name

    def __render_name(self, cr, rect):                                           
        cr.set_source_rgb(1, 1, 1 )                                             
        cr.rectangle(rect.x, rect.y, rect.width, rect.height)                   
        cr.fill()

        draw_text(cr, 
                  self.name, 
                  rect.x, 
                  rect.y, 
                  rect.width, 
                  rect.height)

    def get_height(self):
        return self.ITEM_HEIGHT

    def get_column_widths(self):
        return [self.NAME_WIDTH]

    def get_column_renders(self):
        return [self.__render_name]

gobject.type_register(DeviceItem)

class TrayBluetoothPlugin(object):
    def __init__(self):
        self.my_bluetooth = MyBluetooth(self.__on_adapter_removed, 
                                        self.__on_default_adapter_changed)
        self.width = DeviceItem.NAME_WIDTH
        self.ori_height = 95
        self.height = self.ori_height
        self.device_items = []

        self.__get_devices()

    def __on_adapter_removed(self):
        self.tray_icon.set_visible(False)

    def __on_default_adapter_changed(self):
        self.tray_icon.set_visible(True)

    def init_values(self, this_list):
        self.this = this_list[0]
        self.tray_icon = this_list[1]
        self.tray_icon.set_icon_theme("enable")
        
        if self.my_bluetooth.adapter:
            if self.my_bluetooth.adapter.get_powered():
                self.__get_devices()
            else:
                self.tray_icon.set_visible(False)
        else:
            self.tray_icon.set_visible(False)

    def id(slef):
        return "deepin-bluetooth-plugin-hailongqiu"

    def run(self):
        return True

    def insert(self):
        pass

    def __adapter_toggled(self, widget):
        if self.my_bluetooth.adapter == None:
            return

        self.my_bluetooth.adapter.set_powered(widget.get_active())

    def __bluetooth_selected(self, widget, event):                                 
        self.this.hide_menu()                         
        run_command("deepin-system-settings bluetooth")

    def __get_devices(self):
        devices = self.my_bluetooth.get_devices()                               
        device_count = len(devices)                                                                        
        i = 0
       
        self.device_items = []
        while i < device_count:
            self.device_items.append(DeviceItem(devices[i].get_name()))
            i += 1

        self.height = self.ori_height
        if device_count:
            self.height += device_count * DeviceItem.ITEM_HEIGHT

    def plugin_widget(self):
        plugin_box = gtk.VBox()
        adapter_box = gtk.HBox(spacing = 5)
        adapter_image = ImageBox(app_theme.get_pixbuf("bluetooth/enable_open.png"))
        adapter_label = self.__setup_label(_("Adapter"))
        adapter_toggle = self.__setup_toggle()
        if self.my_bluetooth.adapter:
            adapter_toggle.set_active(self.my_bluetooth.adapter.get_powered())
        adapter_toggle.connect("toggled", self.__adapter_toggled)
        separator_align = self.__setup_align(padding_bottom = 3)
        separator = self.__setup_separator()
        separator_align.add(separator)
        '''
        devices treeview
        '''
        device_treeview = TreeView()
        device_separator_align = self.__setup_align()                           
        device_separator = self.__setup_separator()                             
        device_separator_align.add(device_separator)
        device_count = len(self.device_items)
        if device_count:
            device_treeview.delete_all_items()
            device_treeview.add_items(self.device_items)
            device_treeview.set_size_request(self.width, device_count * DeviceItem.ITEM_HEIGHT)
        else:
            device_treeview.set_child_visible(False)
            device_separator_align.set_child_visible(False)
        '''
        select button
        '''
        select_button_align = self.__setup_align()
        select_button = SelectButton(_("Advanced option..."),             
                                     font_size = 10,                            
                                     ali_padding = 5)                           
        select_button.set_size_request(self.width, 25)                          
        select_button.connect("button-press-event", self.__bluetooth_selected)
        select_button_align.add(select_button)
        
        adapter_box.pack_start(adapter_image, False, False)
        adapter_box.pack_start(adapter_label, False, False)
        adapter_box.pack_start(adapter_toggle, False, False)
        
        plugin_box.pack_start(adapter_box, False, False)
        plugin_box.pack_start(separator_align, False, False)
        plugin_box.pack_start(device_treeview, False, False)
        plugin_box.pack_start(device_separator_align, False, False)
        plugin_box.pack_start(select_button_align, False, False)
        
        return plugin_box

    def show_menu(self):
        self.this.set_size_request(self.width, self.height)

    def hide_menu(self):
        pass

    def __setup_align(self, 
                      xalign=0, 
                      yalign=0, 
                      xscale=0, 
                      yscale=0,                
                      padding_top=5,                                 
                      padding_bottom=0,                                            
                      padding_left=0,                       
                      padding_right=0):                                           
        align = gtk.Alignment()                                                    
        align.set(xalign, yalign, xscale, yscale)                                  
        align.set_padding(padding_top, padding_bottom, padding_left, padding_right)
        return align

    def __setup_label(self, text="", width=50, align=ALIGN_START):                  
        return Label(text, None, 9, align, width, False, False, False)

    def __setup_toggle(self):                                                      
        return ToggleButton(app_theme.get_pixbuf("toggle_button/inactive_normal.png"), 
            app_theme.get_pixbuf("toggle_button/active_normal.png"),               
            inactive_disable_dpixbuf = app_theme.get_pixbuf("toggle_button/inactive_normal.png"))

    def __setup_separator(self):                                                   
        hseparator = HSeparator(app_theme.get_shadow_color("hSeparator").get_color_info(), 0, 0)
        hseparator.set_size_request(100, 3)                                       
        return hseparator

def return_plugin():
    return TrayBluetoothPlugin
