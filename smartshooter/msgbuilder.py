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

class MSGBuilder:
    def __init__(self):
        self.ref_num = 0

    def __create_msg(self, msg_id):
        msg = {}
        msg["msg_type"] = "Request"
        msg["msg_id"] = msg_id
        msg["msg_ref_num"] = self.ref_num
        self.ref_num += 1
        return msg

    def build_SetConfig(self, key, value):
        msg = self.__create_msg("SetConfig")
        msg["ConfigKey"] = key
        msg["ConfigValue"] = value
        return json.dumps(msg)

    def build_Synchronise(self):
        msg = self.__create_msg("Synchronise")
        return json.dumps(msg)

    def build_Shoot(self):
        msg = self.__create_msg("Shoot")
        msg["CameraSelection"] = "All"
        return json.dumps(msg)
