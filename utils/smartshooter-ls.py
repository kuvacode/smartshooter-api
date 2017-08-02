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

def send_synchronise(socket):
    req = {}
    req["msg_type"] = "Request"
    req["msg_id"] = "SynchroniseMsg"
    req["msg_ref_num"] = 0
    socket.send_string(json.dumps(req))
    rep = socket.recv()
    str_msg = rep.decode("utf-8-sig")
    json_msg = json.loads(str_msg)
    return json_msg["Result"]

def print_ls(msg):
    cameras = msg["CameraUpdatedMsg"]
    for camera in cameras:
        print("{0} {1} {2} {3}".format(camera["CameraSerialNumber"],
                                       camera["CameraMake"],
                                       camera["CameraModel"],
                                       camera["CameraName"]))

def main():
    parser = argparse.ArgumentParser("smartshooter-ls.py")
    parser.add_argument("-p", "--publisher",
                        default="tcp://127.0.0.1:54543",
                        metavar="ENDPOINT",
                        help="specify ZMQ address of Smart Shooter publisher")
    parser.add_argument("-r", "--reqrep",
                        default="tcp://127.0.0.1:54544",
                        metavar="ENDPOINT",
                        help="specify ZMQ address of Smart Shooter request/reply server")
    args = parser.parse_args()

    context = zmq.Context()

    req_socket = context.socket(zmq.REQ)
    req_socket.connect(args.reqrep)

    sub_socket = context.socket(zmq.SUB)
    sub_socket.setsockopt(zmq.SUBSCRIBE, b"")
    sub_socket.connect(args.publisher)

    if not send_synchronise(req_socket):
        print("Failed to send synchronise message", file=sys.stderr)
        exit(1)

    while (True):
        raw = sub_socket.recv()
        str_msg = raw.decode("utf-8-sig")
        json_msg = json.loads(str_msg)
        if json_msg["msg_id"] == "SynchroniseMsg":
            print_ls(json_msg)
            return

if __name__ == "__main__":
    main()
