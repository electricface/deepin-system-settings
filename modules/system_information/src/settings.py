#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Long Changjin
# 
# Author:     Long Changjin <admin@longchangjin.cn>
# Maintainer: Long Changjin <admin@longchangjin.cn>
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

import platform
import gtop
import gio
from socket import gethostname

def get_os_version():
    '''
    get the os's name and version
    @return: a string for the os info
    '''
    dist = platform.linux_distribution()
    return "%s %s %s" % (dist[0], dist[1], dist[2])

def get_cpu_info():
    '''
    get the cpu info
    @return: a string for cpu info
    '''
    s = gtop.sysinfo()
    model = {}
    for n in s:
        if "model name" in n:
            if not n["model name"] in model:
                model[n["model name"]] = 1
            else:
                model[n["model name"]] += 1
    if model:
        info = ""
        for k in model:
            info += "%s×%d  " % (k, model[k])
        return info
    else:
        return "--"

def get_mem_info():
    '''
    get the memory info
    @return: a float num for the total memory GB value
    '''
    return round(gtop.mem().dict()['total'] / 1024.0 / 1024 / 1024, 2)

def get_os_arch():
    '''
    get the os's architecture
    @return: a string of the architecture
    '''
    return platform.architecture()[0]

def get_disk_size():
    '''
    get the system disk's size
    @return: a float num
    '''
    f = gio.File('/')
    info = f.query_filesystem_info("*")
    attrs = info.list_attributes()
    if 'filesystem::size' in attrs:
        return round(info.get_attribute_uint64('filesystem::size') / 1024.0 / 1024 / 1024, 3)
    else:
        return 0

def get_hostname():
    '''
    get your own hostname
    @return: a string for hostname
    '''
    return gethostname()