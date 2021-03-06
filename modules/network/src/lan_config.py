#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Zeng Zhi
# 
# Author:     Zeng Zhi <zengzhilg@gmail.com>
# Maintainer: Zeng Zhi <zengzhilg@gmail.com>
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
#from dss import app_theme
from nm_modules import nm_module
from dtk.ui.button import Button
from nmlib.nm_utils import TypeConvert
from nmlib.nm_remote_connection import NMRemoteConnection
from ipsettings import IPV4Conf, IPV6Conf
from elements import SettingSection, TableAsm
import gtk

from shared_methods import Settings, net_manager
from helper import Dispatcher, event_manager
from nls import _
wired_device = []
from dss_log import log

class WiredSetting(Settings):
    def __init__(self, device, spec_connection=None):
        Settings.__init__(self, Sections)
        self.crumb_name = _("Wired")
        self.device = device
        self.spec_connection = spec_connection
        event_manager.emit("update-delete-button", False)

    def get_connections(self):
        self.connections = nm_module.nm_remote_settings.get_wired_connections()

        if self.connections == []:
            self.connections = [nm_module.nm_remote_settings.new_wired_connection()]
        return self.connections
    
    def add_new_connection(self):
        return (nm_module.nm_remote_settings.new_wired_connection(), -1)
    
    def save_changes(self, connection):
        if connection.check_setting_finish():
            if isinstance(connection, NMRemoteConnection):
                connection.update()
            else:
                connection = nm_module.nm_remote_settings.new_connection_finish(connection.settings_dict, 'lan')
                net_manager.set_primary_wire(self.device, connection)

                Dispatcher.emit("connection-replace", connection)
                # reset index
            self.set_button("apply", True)
            Dispatcher.to_main_page()
        else:
            raise "not complete"

    def apply_changes(self, connection):
        wired_device = net_manager.device_manager.get_wired_devices()[0]
        if wired_device.get_state() != 20:
            nm_module.nmclient.activate_connection_async(connection.object_path,
                                               wired_device.object_path,
                                               "/")
            self.device_ethernet = nm_module.cache.get_spec_object(wired_device.object_path)
            self.device_ethernet.emit("try-activate-begin")
        Dispatcher.to_main_page()

class Sections(gtk.Alignment):

    def __init__(self, connection, set_button, settings_obj=None):
        gtk.Alignment.__init__(self, 0, 0 ,0, 0)
        self.set_padding(35, 0, 20, 0)
        self.connection = connection
        self.set_button = set_button
        # 新增settings_obj变量，用于访问shared_methods.Settings对象
        self.settings_obj = settings_obj
        
        if isinstance(connection, NMRemoteConnection):
            net_manager.set_primary_wire(settings_obj.device, connection)

        self.main_box = gtk.VBox()

        basic = SettingSection(_("Wired"), always_show=True)
        button = Button(_("Advanced"))
        button.connect("clicked", self.show_more_options)

        align = gtk.Alignment(0, 0, 0, 0)
        align.set_padding(0, 0, 285, 0)
        align.add(button)

        basic.load([Wired(self.connection, self.set_button, settings_obj), align])
        self.main_box.pack_start(basic, False, False)
        self.add(self.main_box)
        
    def show_more_options(self, widget):
        self.settings_obj.initial_lock = True
        widget.destroy()
        ipv4 = SettingSection(_("IPv4 settings"), always_show=True)
        ipv6 = SettingSection(_("IPv6 settings"), always_show=True)
        ipv4.load([IPV4Conf(self.connection, self.set_button, settings_obj=self.settings_obj, link_local=True)])
        ipv6.load([IPV6Conf(self.connection, self.set_button, settings_obj=self.settings_obj, link_local=True)])

        self.main_box.pack_start(ipv4, False, False, 15)
        self.main_box.pack_start(ipv6, False, False)
        self.settings_obj.initial_lock = False
        

class Wired(gtk.VBox):
    ENTRY_WIDTH = 222

    def __init__(self, connection, set_button_callback=None, settings_obj=None):
        gtk.VBox.__init__(self)
        self.tab_name = _("Wired")
        
        self.ethernet = connection.get_setting("802-3-ethernet")
        self.connection = connection
        self.set_button = set_button_callback
        # 新增settings_obj变量，用于访问shared_methods.Settings对象
        self.settings_obj = settings_obj
        self.settings_obj.initial_lock = True
        #self.settings_obj.set_button("save", True)

        self.__init_table()
        self.__init_signals()

        (mac, clone_mac, mtu) = self.ethernet.mac_address, self.ethernet.cloned_mac_address, self.ethernet.mtu
        if mac != None:
            self.mac_entry.set_address(mac)
        if clone_mac !=None:
            self.clone_entry.set_address(clone_mac)
        if mtu != None:
            self.mtu_spin.set_value(int(mtu))
        
        # check valid for nmconnection init
        #if not type(self.connection) == NMRemoteConnection:
            #self.save_settings(None, None, None)
        self.settings_obj.initial_lock = False

    def __init_table(self):
        self.table = TableAsm()
        self.mac_entry = self.table.row_mac_entry(_("Device Mac Address:"))
        self.clone_entry = self.table.row_mac_entry(_("Cloned Mac Address:"))
        self.mtu_spin = self.table.row_spin(_("MTU:"), 0, 1500)
        self.table.table_build()
        # TODO UI change
        align = gtk.Alignment(0,0,0,0)
        align.add(self.table)
        self.pack_start(align)
   
    def __init_signals(self):
        self.mac_entry.connect("changed", self.save_settings, "mac_address")
        self.clone_entry.connect("changed", self.save_settings, "cloned_mac_address")
        self.mtu_spin.connect("value_changed", self.save_settings, "mtu")
        self.mtu_spin.value_entry.connect("changed", self.spin_user_set)

    def spin_user_set(self, widget, value):
        if value == "":
            return
        value = int(value)
        if self.mtu_spin.lower_value <= value <= self.mtu_spin.upper_value:
            self.mtu_spin.update_and_emit(value)
        elif value < self.mtu_spin.lower_value:
            self.mtu_spin.update_and_emit(self.mtu_spin.lower_value)
        else:
            self.mtu_spin.update_and_emit(self.mtu_spin.upper_value)

        ## retrieve wired info
    def save_settings(self, widget, content, types):
        #value = None
        if types:
            setattr(self.ethernet, types, content)
        if self.settings_obj is None:
            return
        
        # check mac address whether is valid
        if types == "mac_address":
            mac_address = content
            cloned_mac_address = self.clone_entry.get_address()
        elif types == "cloned_mac_address":
            mac_address = self.mac_entry.get_address()
            cloned_mac_address = content
        else:
            mac_address = self.mac_entry.get_address()
            cloned_mac_address = self.clone_entry.get_address()

        if (mac_address == ":::::") or \
                (mac_address == "") or \
                (TypeConvert.is_valid_mac_address(mac_address)):
            mac_address_is_valid = True
        else:
            mac_address_is_valid = False
        if (cloned_mac_address == ":::::") or \
                (cloned_mac_address == "") or \
                (TypeConvert.is_valid_mac_address(cloned_mac_address)):
            cloned_mac_address_is_valid = True
        else:
            cloned_mac_address_is_valid = False
        if mac_address_is_valid and cloned_mac_address_is_valid:
            self.settings_obj.mac_is_valid = True
        else:
            self.settings_obj.mac_is_valid = False

        # 统一调用shared_methods.Settings的set_button
        log.debug('set_button True')
        self.settings_obj.set_button("save", True)

        """
        if type(value) is str and value:
            if TypeConvert.is_valid_mac_address(value):
                #widget.set_normal()
                #self.queue_draw()
                setattr(self.ethernet, types, value)
                if self.connection.check_setting_finish():
                    self.set_button("save", True)
            else:
                Dispatcher.set_tip("invalid mac address, please check your settings") 
                #widget.set_warning()
                #self.queue_draw()
                self.set_button("save", False)
                if value is "":
                    #delattr(self.ethernet, types)
                    self.set_button("save", True)
        else:
            setattr(self.ethernet, types, value)
            if self.connection.check_setting_finish():
                self.set_button("save", True)
        """
