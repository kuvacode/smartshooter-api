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

import json
from .selection import CameraSelection

class MSGBuilder:
    def __init__(self):
        self.__seq_num = 0

    def __create_msg(self, msg_id):
        msg = {}
        msg["msg_type"] = "Request"
        msg["msg_id"] = msg_id
        msg["msg_seq_num"] = self.__seq_num
        self.__seq_num += 1
        return msg

    def __add_selection(self, msg, selection):
        mode = selection.get_mode()
        msg["CameraSelection"] = mode
        if mode == "Single":
            msg["CameraKey"] = selection.get_key()
        elif mode == "Group":
            msg["CameraGroup"] = selection.get_group()
        elif mode == "Multiple":
            msg["CameraKeys"] = selection.get_keys()

    def build_SetConfig(self, key, value):
        msg = self.__create_msg("SetConfig")
        msg["ConfigKey"] = key
        msg["ConfigValue"] = value
        return json.dumps(msg)

    def build_Synchronise(self):
        msg = self.__create_msg("Synchronise")
        return json.dumps(msg)

    def build_Connect(self, selection):
        msg = self.__create_msg("Connect")
        self.__add_selection(msg, selection)
        return json.dumps(msg)

    def build_Disconnect(self, selection):
        msg = self.__create_msg("Disconnect")
        self.__add_selection(msg, selection)
        return json.dumps(msg)

    def build_Shoot(self, selection, bulb_timer, photo_origin):
        msg = self.__create_msg("Shoot")
        self.__add_selection(msg, selection)
        if bulb_timer:
            msg["BulbTimer"] = bulb_timer
        if photo_origin:
            msg["PhotoOrigin"] = photo_origin
        return json.dumps(msg)

    def build_SetProperty(self, selection, prop, value):
        msg = self.__create_msg("SetProperty")
        self.__add_selection(msg, selection)
        msg["CameraPropertyType"] = prop.name
        msg["CameraPropertyValue"] = value
        return json.dumps(msg)

    def build_LiveviewFocus(self, selection, focus_step):
        msg = self.__create_msg("LiveviewFocus")
        self.__add_selection(msg, selection)
        msg["CameraLiveviewFocusStep"] = focus_step
        return json.dumps(msg)
