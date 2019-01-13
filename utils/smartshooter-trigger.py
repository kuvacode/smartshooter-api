#!/usr/bin/env python3
#
# Copyright (c) 2015-2017, Kuvacode Oy. All rights reserved.
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

import sys
import json
import argparse
import zmq

def send_shoot(socket):
    req = {}
    req["msg_type"] = "Request"
    req["msg_id"] = "Shoot"
    req["msg_ref_num"] = 0
    req["CameraSelection"] = "All"
    socket.send_string(json.dumps(req))
    rep = socket.recv()
    str_msg = rep.decode("utf-8-sig")
    json_msg = json.loads(str_msg)
    return json_msg["Result"]

def main():
    parser = argparse.ArgumentParser("smartshooter-trigger.py")
    parser.add_argument("-r", "--reqrep",
                        default="tcp://127.0.0.1:54544",
                        metavar="ENDPOINT",
                        help="specify ZMQ address of Smart Shooter request/reply server")
    args = parser.parse_args()

    context = zmq.Context()

    req_socket = context.socket(zmq.REQ)
    req_socket.connect(args.reqrep)

    if not send_shoot(req_socket):
        print("Failed to send trigger message", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()
