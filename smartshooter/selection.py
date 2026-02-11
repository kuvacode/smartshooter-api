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

from .enums import PhotoSelectionMode
from .enums import CameraSelectionMode

class CameraSelection:
    def __init__(self):
        self.__mode = CameraSelectionMode.All
        self.__key = None
        self.__keys = []
        self.__group = None

    def select_camera(self, key):
        self.__mode = CameraSelectionMode.Single
        self.__key = key
        self.__keys = None
        self.__group = None

    def select_cameras(self, keys):
        self.__mode = CameraSelectionMode.Multiple
        self.__key = None
        self.__keys = keys
        self.__group = None

    def select_all_cameras(self):
        self.__mode = CameraSelectionMode.All
        self.__key = None
        self.__keys = None
        self.__group = None

    def select_camera_group(self, group):
        self.__mode = CameraSelectionMode.Group
        self.__key = None
        self.__keys = None
        self.__group = group

    def get_mode(self):
        return self.__mode

    def get_key(self):
        return self.__key

    def get_keys(self):
        return self.__keys

    def get_group(self):
        return self.__group

class PhotoSelection:
    def __init__(self):
        self.__mode = PhotoSelectionMode.All
        self.__key = None
        self.__keys = []

    def select_photo(self, key):
        self.__mode = PhotoSelectionMode.Single
        self.__key = key
        self.__keys = None

    def select_photos(self, keys):
        self.__mode = PhotoelectionMode.Multiple
        self.__key = None
        self.__keys = keys

    def select_all_photos(self):
        self.__mode = PhotoSelectionMode.All
        self.__key = None
        self.__keys = None

    def get_mode(self):
        return self.__mode

    def get_key(self):
        return self.__key

    def get_keys(self):
        return self.__keys
