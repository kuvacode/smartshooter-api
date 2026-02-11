#
# Copyright (c) 2019-2026, Kuvacode Oy. All rights reserved.
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

from .enums import CameraSelectionMode
from .enums import PhotoSelectionMode
from .selection import CameraSelection
from .selection import PhotoSelection

class StateTracker:
    def __init__(self):
        self.__is_synchronised = False
        self.__cameras = dict()
        self.__photos = dict()

    def is_synchronised(self):
        return self.__is_synchronised

    def invalidate(self):
        self.__is_synchronised = False

    def __read_Synchronise(self, msg):
        self.__is_synchronised = True
        cameras = msg["CameraInfo"]
        for camera in cameras:
            self.__read_CameraUpdated(camera)
        photos = msg["PhotoInfo"]
        for photo in photos:
            self.__read_PhotoUpdated(photo)

    def __read_CameraUpdated(self, msg):
        key = msg["CameraKey"]
        if key not in self.__cameras:
            self.__cameras[key] = dict()
            self.__cameras[key]["CameraPropertyInfo"] = dict()
        obj = self.__cameras[key]
        for key, value in msg.items():
            if key != "CameraPropertyInfo":
                obj[key] = value
            else:
                for propinfo in value:
                    proptype = propinfo["CameraPropertyType"]
                    if proptype not in obj["CameraPropertyInfo"]:
                        obj["CameraPropertyInfo"][proptype] = dict()
                    obj["CameraPropertyInfo"][proptype].update(propinfo)

    def __read_PhotoUpdated(self, msg):
        key = msg["PhotoKey"]
        if key not in self.__photos:
            self.__photos[key] = dict()
        obj = self.__photos[key]
        for key, value in msg.items():
            obj[key] = value

    def process_reply(self, msg):
        if msg["msg_id"] == "Synchronise":
            self.__read_Synchronise(msg)

    def process_event(self, msg):
        if msg["msg_id"] == "CameraUpdated":
            self.__read_CameraUpdated(msg)

    def get_camera_list(self):
        return list(self.__cameras)

    def get_photo_list(self):
        return list(self.__photos)

    def get_camera_info(self, key):
        return self.__cameras[key]

    def get_photo_info(self, key):
        return self.__photos[key]

    def get_selected_cameras(self, selection):
        mode = selection.get_mode()
        if mode == CameraSelectionMode.All:
            return self.get_camera_list()
        elif mode == CameraSelectionMode.Single:
            return [selection.get_key()]
        elif mode == CameraSelectionMode.Multiple:
            return [selection.get_keys()]
        elif mode == CameraSelectionMode.Group:
            selected_cameras = []
            for key, value in self.__cameras.items():
                if value["CameraGroup"] == selection.get_group():
                    selected_cameras.append(key)
            return selected_cameras
        return []

    def get_selected_photos(self, selection):
        mode = selection.get_mode()
        if mode == PhotoSelectionMode.All:
            return self.get_photo_list()
        elif mode == PhotoSelectionMode.Single:
            return [selection.get_key()]
        elif mode == PhotoSelectionMode.Multiple:
            return [selection.get_keys()]
        return []

    def __is_camera_connected(self, key):
        camera = self.__cameras[key]
        status = camera["CameraStatus"]
        return status in ["Ready", "Busy"]

    def __get_active_camera(self, selection):
        mode = selection.get_mode()
        if mode == CameraSelectionMode.All:
            for key in self.__cameras:
                if self.__is_camera_connected(key):
                    return key
        elif mode == CameraSelectionMode.Single:
            return selection.get_key()
        elif mode == CameraSelectionMode.Multiple:
            for key in selection.get_keys():
                if self.__is_camera_connected(key):
                    return key
        elif mode == CameraSelectionMode.Group:
            for key, value in self.__cameras.items():
                if self.__is_camera_connected(key):
                    if value["CameraGroup"] == selection.get_group():
                        return key
        return None

    def get_property(self, selection, prop):
        key = self.__get_active_camera(selection)
        camera = self.__cameras[key]
        propinfo = camera["CameraPropertyInfo"][prop.name]
        return propinfo["CameraPropertyValue"]

    def get_property_range(self, selection, prop):
        key = self.__get_active_camera(selection)
        camera = self.__cameras[key]
        propinfo = camera["CameraPropertyInfo"][prop.name]
        return propinfo["CameraPropertyRange"]
