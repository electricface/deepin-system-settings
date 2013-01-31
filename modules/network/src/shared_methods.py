#!/usr/bin/env python
#-*- coding:utf-8 -*-
from nm_modules import nm_module
from nmlib.nmcache import cache
from helper import Dispatcher

DEVICE_UNAVAILABLE = 0
DEVICE_AVAILABLE = 1
DEVICE_DISACTIVE = 1
DEVICE_ACTIVE = 2

class NetManager(object):

    def __init__(self):
        self.wired_devices = nm_module.nmclient.get_wired_devices()
        self.wireless_devices = nm_module.nmclient.get_wireless_devices()
        self.init_signals()

    def init_signals(self):
        if self.wired_devices:
            self.wired_device = self.wired_devices[0]
        if self.wireless_devices:
            self.wireless_device = self.wireless_devices[0]
        self.wired_device.connect("state-changed", self.__wired_state_change)
        self.wireless_device.connect("state-changed", self.__wireless_state_change)

    def __wired_state_change(self, widget, new_state, old_state, reason):
        Dispatcher.wired_change(new_state, reason)

    def __wireless_state_change(self, widget, new_state, old_state, reason):
        Dispatcher.wireless_change(new_state, reason)

    def get_wired_state(self):
        if self.wired_devices is None:
            # 没有有限设备
            return (False, False)
        else:
            if self.wired_device.get_state() == 20:
                return (False, False)
            else:
                return (True, self.wired_device.is_active())

    def active_wired_device(self, actived_cb):
        wired_devices = nm_module.nmclient.get_wired_devices()
        device = wired_devices[0]

        def device_is_active( widget, reason):
            actived_cb()
        device.connect("device-active", device_is_active)

        if not device.is_active():
            connections = nm_module.nm_remote_settings.get_wired_connections()
            if not connections:
                connection = nm_module.nm_remote_settings.new_wired_connection()
                nm_module.nm_remote_settings.new_connection_finish(connection.settings_dict, 'lan')

            device_ethernet = cache.get_spec_object(device.object_path)
            device_ethernet.auto_connect()

    def disactive_wired_device(self, disactived_cb):
        wired_devices = nm_module.nmclient.get_wired_devices()
        device = wired_devices[0]

        def device_is_disactive( widget, reason):
            disactived_cb()
        device.connect("device-deactive", device_is_disactive)
        device.nm_device_disconnect()


    # Wireless
    def get_wireless_state(self):
        wireless_devices = nm_module.nmclient.get_wireless_devices()
        if not wireless_devices:
            return (False, DEVICE_UNAVAILABLE)
        else:
            if not nm_module.nmclient.wireless_get_enabled():
                nm_module.nmclient.wireless_set_enabled(True)
                return (False, DEVICE_AVAILABLE)
            else:
                return (wireless_devices[0].is_active(), DEVICE_AVAILABLE)

    def get_ap_list(self):
        wireless_device = nm_module.nmclient.get_wireless_devices()[0]
        device_wifi = cache.get_spec_object(wireless_device.object_path)
        ap_list = device_wifi.order_ap_list()
        # 返回ap对象，ap.get_ssid() 获取ssid, ap.get_flags()获得加密状态，0为加密，1加密
        return ap_list

    def get_active_connection(self, ap_list):
        wireless_device = nm_module.nmclient.get_wireless_devices()[0]
        index = []
        active_connection = wireless_device.get_active_connection()
        if active_connection:
            index.append([ap.object_path for ap in ap_list].index(active_connection.get_specific_object()))
            return index
        else:
            return []

    def active_wireless_device(self, actived_cb):
        wireless_device = nm_module.nmclient.get_wireless_devices()[0]

        def device_is_active(widget, reason):
            print "active"
            actived_cb()
        wireless_device.connect("device-active", device_is_active)
        device_wifi = cache.get_spec_object(wireless_device.object_path)
        device_wifi.auto_connect()

    def disactive_wireless_device(self, disactived_cb):
        wireless_device = nm_module.nmclient.get_wireless_devices()[0]
        
        def device_is_disactive( widget, reason):
            active = wireless_device.get_active_connection()
            disactived_cb()
        wireless_device.connect("device-deactive", device_is_disactive)
        wireless_device.nm_device_disconnect()
