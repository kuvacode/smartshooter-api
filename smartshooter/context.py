#
# Copyright (c) 2019, Kuvacode Oy. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import os
import sys
import json
import time
from .msgbuilder import MSGBuilder
from .statetracker import StateTracker
from .selection import CameraSelection

def is_embedded():
    exe = os.path.basename(sys.executable)
    return exe.startswith("SmartShooter")

if is_embedded():
    import apphooks
else:
    import zmq

class EmbeddedSocket:
    def __init__(self):
        pass
    def send_request(self, msg):
        apphooks.send_request(msg)
    def recv_reply(self):
        return apphooks.recv_reply()
    def recv_event(self):
        return apphooks.recv_event()

class ZMQSocket:
    def __init__(self):
        self.__ctx = zmq.Context()
        self.__req_socket = self.__ctx.socket(zmq.REQ)
        self.__sub_socket = self.__ctx.socket(zmq.SUB)
        self.__sub_socket.setsockopt(zmq.SUBSCRIBE, b"")
        self.__req_socket.connect("tcp://127.0.0.1:54544")
        self.__sub_socket.connect("tcp://127.0.0.1:54543")
    def send_request(self, msg):
        self.__req_socket.send_string(msg)
    def recv_reply(self):
        return self.__req_socket.recv_string()
    def recv_event(self):
        return self.__sub_socket.recv().decode("utf-8")

class Context:
    def __init__(self):
        self.__is_embedded = is_embedded()
        self.__msgbuilder = MSGBuilder()
        self.__tracker = StateTracker()
        self.__selection = CameraSelection()
        if self.__is_embedded:
            self.__socket = EmbeddedSocket()
        else:
            self.__socket = ZMQSocket()
        self.synchronise()

    def __transact(self, msg):
        self.check_status()
        self.__socket.send_request(msg)
        jstr = self.__socket.recv_reply()
        reply = json.loads(jstr)
        self.__tracker.process_reply(reply)
        return reply

    def __read_event(self):
        self.check_status()
        jstr = self.__socket.recv_event()
        event = json.loads(jstr)
        self.__tracker.process_event(event)

    def check_status(self):
        ok = apphooks.check_status()
        if not ok:
            sys.exit()

    def wait_until(self, target):
        while True:
            self.check_status()
            now = time.time()
            if now >= target:
                return
            diff = target - now
            if diff > 2:
                time.sleep(1)
            else:
                time.sleep(0.01)

    def wait(self, secs):
        target = time.time() + secs
        self.wait_until(target)

    def set_config(self, key, value):
        msg = self.__msgbuilder.build_SetConfig(key, value)
        self.__transact(msg)

    def synchronise(self):
        self.__tracker.invalidate()
        msg = self.__msgbuilder.build_Synchronise()
        self.__transact(msg)

    def get_camera_list(self):
        return self.__tracker.get_camera_list()

    def get_photo_list(self):
        return self.__tracker.get_photo_list()

    def get_camera_info(self, key):
        return self.__tracker.get_camera_info(key)

    def get_photo_info(self, key):
        return self.__tracker.get_photo_info(key)

    def select_camera(self, key):
        self.__selection.select_camera(key)

    def select_cameras(self, keys):
        self.__selection.select_cameras(keys)

    def select_all_cameras(self):
        self.__selection.select_all_cameras()

    def select_camera_group(self, group):
        self.__selection.select_camera_group(group)

    def connect(self):
        msg = self.__msgbuilder.build_Connect(self.__selection)
        self.__transact(msg)

    def disconnect(self):
        msg = self.__msgbuilder.build_Disconnect(self.__selection)
        self.__transact(msg)

    def shoot(self, bulb_ms=None):
        msg = self.__msgbuilder.build_Shoot(self.__selection, bulb_ms)
        self.__transact(msg)

    def set_property(self, prop, value):
        msg = self.__msgbuilder.build_SetProperty(self.__selection, prop, value)
        self.__transact(msg)

    def get_property(self, prop):
        return self.__tracker.get_property(self.__selection, prop)

    def get_property_range(self, prop):
        return self.__tracker.get_property_range(self.__selection, prop)
