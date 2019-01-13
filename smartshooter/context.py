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
        apphooks.send_request(msg);
    def recv_reply(self):
        return apphooks.recv_reply()
    def recv_event(self):
        return apphooks.recv_event()

class ZMQSocket:
    def __init__(self):
        self.ctx = zmq.Context()
        self.req_socket = self.ctx.socket(zmq.REQ)
        self.sub_socket = self.ctx.socket(zmq.SUB)
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, b"")
        self.req_socket.connect("tcp://127.0.0.1:54544")
        self.sub_socket.connect("tcp://127.0.0.1:54543")
    def send_request(self, msg):
        self.req_socket.send_string(msg)
    def recv_reply(self):
        return self.req_socket.recv_string()
    def recv_event(self):
        return self.sub_socket.recv().decode("utf-8");

class Context:
    def __init__(self):
        self.is_synchronised = False
        self.is_embedded = is_embedded()
        self.msgbuilder = MSGBuilder()
        if self.is_embedded:
            self.socket = EmbeddedSocket()
        else:
            self.socket = ZMQSocket()

    def __transact(self, msg):
        self.check_status()
        self.socket.send_request(msg)
        jstr = self.socket.recv_reply()
        reply = json.loads(jstr)
        return reply

    def __read_event(self):
        self.check_status()
        jstr = self.socket.recv_event()
        event = json.loads(jstr)
        if event["msg_id"] == "Synchronise":
            self.is_synchronised = True

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
        msg = self.msgbuilder.build_SetConfig(key, value)
        self.__transact(msg)

    def synchronise(self):
        self.is_synchronised = False
        msg = self.msgbuilder.build_Synchronise()
        self.__transact(msg)
        while not self.is_synchronised:
            self.__read_event()

    def shoot(self):
        msg = self.msgbuilder.build_Shoot()
        self.__transact(msg)
