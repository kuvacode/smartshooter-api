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
from .enums import CameraSelectionMode
from .enums import PhotoSelectionMode
from .selection import CameraSelection
from .selection import PhotoSelection

def is_embedded():
    exe = os.path.basename(sys.executable)
    return exe.startswith("SmartShooter") or exe.startswith("Smart Shooter") or exe.startswith("CaptureGRID")

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
        self.__camera_selection = CameraSelection()
        self.__photo_selection = PhotoSelection()
        if self.__is_embedded:
            self.__socket = EmbeddedSocket()
        else:
            self.__socket = ZMQSocket()
        self.synchronise()

    def __transact(self, msg):
        self.check_status()
        self.__socket.send_request(msg)
        self.__read_events()
        jstr = self.__socket.recv_reply()
        reply = json.loads(jstr)
        self.__tracker.process_reply(reply)
        return reply

    def __read_events(self):
        while True:
            self.check_status()
            jstr = self.__socket.recv_event()
            if not jstr:
                return
            event = json.loads(jstr)
            self.__tracker.process_event(event)

    def check_status(self):
        ok = apphooks.check_status()
        if not ok:
            sys.exit()

    def wait_until(self, target):
        while True:
            self.check_status()
            self.__read_events()
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

    def __wait_for_liveview_enabled(self):
        self.__read_events()
        cameras = []
        for camera in self.get_selected_cameras():
            info = self.get_camera_info(camera)
            status = info["CameraStatus"]
            if status in ["Ready", "Busy"] and not info["CameraLiveviewIsEnabled"]:
                cameras.append(camera)
        num_pending = len(cameras)
        while num_pending > 0:
            self.__read_events()
            for i in range(len(cameras)):
                if cameras[i]:
                    info = self.get_camera_info(cameras[i])
                    status = info["CameraStatus"]
                    if status not in ["Ready", "Busy"]:
                        num_pending -= 1
                        cameras[i] = None
                    elif status == "Ready" and info["CameraLiveviewIsEnabled"]:
                        num_pending -= 1
                        cameras[i] = None

    def __wait_for_liveview_frame(self):
        self.__read_events()
        cameras = []
        markers = []
        for camera in self.get_selected_cameras():
            info = self.get_camera_info(camera)
            status = info["CameraStatus"]
            if status in ["Ready", "Busy"] and info["CameraLiveviewIsEnabled"]:
                cameras.append(camera)
                markers.append(info["CameraLiveviewNumFrames"] + 10)
        num_pending = len(cameras)
        while num_pending > 0:
            self.__read_events()
            for i in range(len(cameras)):
                if cameras[i]:
                    info = self.get_camera_info(cameras[i])
                    status = info["CameraStatus"]
                    if status not in ["Ready", "Busy"] or not info["CameraLiveviewIsEnabled"]:
                        num_pending -= 1
                        cameras[i] = None
                    elif status == "Ready" and info["CameraLiveviewNumFrames"] > markers[i]:
                        num_pending -= 1
                        cameras[i] = None


    def wait_for_liveview(self):
        self.__wait_for_liveview_enabled()
        self.__wait_for_liveview_frame()

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
        self.__camera_selection.select_camera(key)

    def select_cameras(self, keys):
        self.__camera_selection.select_cameras(keys)

    def select_all_cameras(self):
        self.__camera_selection.select_all_cameras()

    def select_camera_group(self, group):
        self.__camera_selection.select_camera_group(group)

    def get_selected_cameras(self):
        return self.__tracker.get_selected_cameras(self.__camera_selection);

    def select_photo(self, key):
        self.__photo_selection.select_photo(key)

    def select_photos(self, keys):
        self.__photo_selection.select_photos(keys)

    def select_all_photos(self):
        self.__photo_selection.select_all_photos()

    def get_selected_photos(self):
        return self.__tracker.get_selected_photos(self.__photo_selection);

    def connect(self):
        msg = self.__msgbuilder.build_Connect(self.__camera_selection)
        self.__transact(msg)

    def disconnect(self):
        msg = self.__msgbuilder.build_Disconnect(self.__camera_selection)
        self.__transact(msg)

    def shoot(self, bulb_timer=None, photo_origin="api"):
        msg = self.__msgbuilder.build_Shoot(self.__camera_selection, bulb_timer, photo_origin)
        self.__transact(msg)

    def autofocus(self):
        msg = self.__msgbuilder.build_Autofocus(self.__camera_selection)
        self.__transact(msg)

    def set_property(self, prop, value):
        msg = self.__msgbuilder.build_SetProperty(self.__camera_selection, prop, value)
        self.__transact(msg)

    def set_shutter_button(self, button):
        msg = self.__msgbuilder.build_SetShutterButton(self.__camera_selection, button)
        self.__transact(msg)

    def enable_liveview(self, enable):
        msg = self.__msgbuilder.build_EnableLiveview(self.__camera_selection, enable)
        self.__transact(msg)

    def move_focus(self, focus_step):
        msg = self.__msgbuilder.build_LiveviewFocus(self.__camera_selection, focus_step)
        self.__transact(msg)

    def position_power_zoom(self, position):
        msg = self.__msgbuilder.build_PowerZoomPosition(self.__camera_selection, position)
        self.__transact(msg)

    def stop_power_zoom(self, position):
        msg = self.__msgbuilder.build_PowerZoomStop(self.__camera_selection)
        self.__transact(msg)

    def engage_latch(self, latch_index):
        msg = self.__msgbuilder.build_EngageLatch(self.__camera_selection, latch_index)
        self.__transact(msg)

    def release_latch(self, latch_index):
        msg = self.__msgbuilder.build_ReleaseLatch(latch_index)
        self.__transact(msg)

    def cancel_latch(self, latch_index):
        msg = self.__msgbuilder.build_CancelLatch(latch_index)
        self.__transact(msg)

    def engage_trigger(self):
        msg = self.__msgbuilder.build_EngageTrigger(self.__camera_selection)
        self.__transact(msg)

    def release_trigger(self, trigger_interval):
        msg = self.__msgbuilder.build_ReleaseTrigger(trigger_interval)
        self.__transact(msg)

    def cancel_trigger(self):
        msg = self.__msgbuilder.build_CancelTrigger()
        self.__transact(msg)

    def get_property(self, prop):
        return self.__tracker.get_property(self.__camera_selection, prop)

    def get_property_range(self, prop):
        return self.__tracker.get_property_range(self.__camera_selection, prop)

    def is_camera_connected(self):
        for camera in self.get_selected_cameras():
            info = self.get_camera_info(camera)
            status = info["CameraStatus"]
            if status not in ["Ready", "Busy"]:
                return False
        return True

    def is_liveview_enabled(self):
        for camera in self.get_selected_cameras():
            info = self.get_camera_info(camera)
            status = info["CameraStatus"]
            if status not in ["Ready", "Busy"] or not info["CameraLiveviewIsEnabled"]:
                return False
        return True
