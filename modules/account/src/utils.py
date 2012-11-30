#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 ~ 2013 Deepin, Inc.
#               2012 ~ 2013 Long Wei
#
# Author:     Long Wei <yilang2007lw@gmail.com>
# Maintainer: Long Wei <yilang2007lw@gmail.com>
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

import polkit_permission as polkitpermission

import dbus
import gobject
import re
import traceback

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default = True)

name_re = re.compile("[0-9a-zA-Z-]*")

system_bus = dbus.SystemBus()

def valid_object_path(object_path):
    if not isinstance(object_path, str):
        return False

    if not object_path.startswith("/"):
        return False

    return all(map(lambda x:name_re.match(x), object_path.split(".")))    

class InvalidPropType(Exception):
    
    def __init__(self, prop_name, need_type, real_type = "string"):
        self.prop_name = prop_name
        self.need_type = need_type
        self.real_type = real_type

    def __str__(self):
        return repr("property %s need type %s ,but given type is :%s",
                    (self.prop_name, self.need_type, self.real_type))

class InvalidObjectPath(Exception):
    
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return repr("InvalidObjectPath:" + self.path)


class BusBase(gobject.GObject):
    
    def __init__(self, path, interface, service = "org.freedesktop.Accounts", bus = system_bus):
        gobject.GObject.__init__(self)
        if valid_object_path(path):
            self.object_path = path
        else:
            raise InvalidObjectPath(path)

        self.object_interface = interface
        self.service = service
        self.bus = bus

        try:
            self.dbus_proxy = self.bus.get_object(self.service, self.object_path)
            self.dbus_interface = dbus.Interface(self.dbus_proxy, self.object_interface)
        except dbus.exceptions.DBusException:
            traceback.print_exc()

    def init_dbus_properties(self):        
        try:
            self.properties_interface = dbus.Interface(self.dbus_proxy, "org.freedesktop.DBus.Properties" )
        except dbus.exceptions.DBusException:
            traceback.print_exc()

        if self.properties_interface:
            try:
                self.properties = self.properties_interface.GetAll(self.object_interface)
            except:
                print "get properties failed"
                traceback.print_exc()

    def dbus_method(self, method_name, *args, **kwargs):
        try:
            return apply(getattr(self.dbus_interface, method_name), args, kwargs)
        except dbus.exceptions.DBusException, e:
            if "org.freedesktop.Accounts.Error.PermissionDenied" in e:
                pass
            elif "org.freedesktop.Accounts.Error.UserExists" in e:
                pass
            elif "org.freedesktop.Accounts.Error.Failed" in e:
                pass
            else:
                traceback.print_exc()

    def call_async(self, method_name, *args, **kwargs):
        try:
            return apply(getattr(self.dbus_interface, method_name), args, kwargs)
        except dbus.exceptions.DBusException, e:
            if "org.freedesktop.Accounts.Error.PermissionDenied" in e:
                pass
            elif "org.freedesktop.Accounts.Error.UserExists" in e:
                pass
            elif "org.freedesktop.Accounts.Error.Failed" in e:
                pass
            else:
                traceback.print_exc()

class PolkitPermission:
    
    def __init__(self, action, subject = "subject"):
        self.permission =  polkitpermission.new(action)
    
    def get_action_id(self):
        return self.permission.get_action_id()

    # def get_subject(self):
    #     return self.permission.get_subject()

    def get_allowed(self):
        return self.permission.get_allowed()

    def get_can_acquire(self):
        return self.permission.get_can_acquire()

    def get_can_release(self):
        return self.permission.get_can_release()
    
    def acquire(self):
        if self.get_can_acquire():
            return self.permission.acquire()
        else:
            pass

    def release(self):
        if self.get_can_release():
            return self.permission.release()
        else:
            pass

if __name__ == "__main__":
    permission = PolkitPermission("org.freedesktop.accounts.user-administration")
    print "action_id:"
    print permission.get_action_id()
    print "allowed:"
    print permission.get_allowed()
    print "can_acuire:"
    print permission.get_can_acquire()
    print "can_release:"
    print permission.get_can_release()

    permission.acquire()
