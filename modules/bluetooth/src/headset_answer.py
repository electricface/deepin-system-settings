#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2013 Deepin, Inc.
#               2011 ~ 2013 Wang YaoHua
# 
# Author:     Wang YaoHua <mr.asianwang@gmail.com>
# Maintainer: Wang YaoHua <mr.asianwang@gmail.com>
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

import dbus
session_bus = dbus.SessionBus()
from bt.bus_utils import BusBase

class HeadsetAnswer(BusBase):
    def __init__(self):
        BusBase.__init__(self, path = "/com/deepin/bluetooth", interface = "com.deepin.BluetoothHeadset", 
                         service="com.deepin.BluetoothHeadset", bus=session_bus)

    def send_answer_request(self):
        return self.dbus_method("SendAnswerReqest")

headset_answer = HeadsetAnswer()
