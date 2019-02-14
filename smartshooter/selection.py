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

class CameraSelection:
    def __init__(self):
        self.__mode = "All"
        self.__key = None
        self.__keys = []
        self.__group = None

    def select_camera(self, key):
        self.__mode = "Single"
        self.__key = key
        self.__keys = None
        self.__group = None

    def select_cameras(self, keys):
        self.__mode = "Multiple"
        self.__key = None
        self.__keys = keys
        self.__group = None

    def select_all_cameras(self):
        self.__mode = "All"
        self.__key = None
        self.__keys = None
        self.__group = None

    def select_camera_group(self, group):
        self.__mode = "Group"
        self.__key = None
        self.__keys = None
        self.__group = group

    def get_mode(self):
        return self.__mode

    def get_key():
        return self.__key

    def get_keys():
        return self.__keys

    def get_group():
        return self.__group
