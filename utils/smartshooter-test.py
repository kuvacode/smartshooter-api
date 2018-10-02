#!/usr/bin/env python3
#
# Copyright (c) 2018, Kuvacode Oy. All rights reserved.
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

msg_ref_num = 0

def send_request(socket, req):
    global msg_ref_num
    req["msg_ref_num"] = msg_ref_num
    msg_ref_num += 1
    text = json.dumps(req)
    print(text)
    socket.send_string(text)
    rep = socket.recv()
    text = rep.decode("utf-8-sig")
    print(text)
    msg = json.loads(text)
    return msg["Result"]

def send_synchronise(socket):
    req = {}
    req["msg_type"] = "Request"
    req["msg_id"] = "Synchronise"
    return send_request(socket, req)

def send_connect(socket, camera_key):
    req = {}
    req["msg_type"] = "Request"
    req["msg_id"] = "Connect"
    req["CameraSelection"] = "Single"
    req["CameraKey"] = camera_key
    return send_request(socket, req)

def send_autofocus(socket, camera_key):
    req = {}
    req["msg_type"] = "Request"
    req["msg_id"] = "Autofocus"
    req["CameraSelection"] = "Single"
    req["CameraKey"] = camera_key
    return send_request(socket, req)

def send_setproperty(socket, camera_key, prop, value):
    req = {}
    req["msg_type"] = "Request"
    req["msg_id"] = "SetProperty"
    req["CameraSelection"] = "Single"
    req["CameraKey"] = camera_key
    req["CameraPropertyType"] = prop
    req["CameraPropertyValue"] = value 
    return send_request(socket, req)

def send_shoot(socket, camera_key):
    req = {}
    req["msg_type"] = "Request"
    req["msg_id"] = "Shoot"
    req["CameraSelection"] = "Single"
    req["CameraKey"] = camera_key
    return send_request(socket, req)

def send_download(socket, photo_key):
    req = {}
    req["msg_type"] = "Request"
    req["msg_id"] = "Download"
    req["PhotoSelection"] = "Single"
    req["PhotoKey"] = photo_key
    return send_request(socket, req)

def wait_for(sub_socket, msg_id):
    while (True):
        raw = sub_socket.recv()
        text = raw.decode("utf-8-sig")
        msg = json.loads(text)
        if msg["msg_id"] != "NetworkPing":
            print("event:    {} {}".format(msg["msg_ref_num"], msg["msg_id"]))
        if msg["msg_id"] == msg_id:
            return msg

def wait_for_Synchonise(sub_socket):
    print("wait for: Synchonise")
    return wait_for(sub_socket, "Synchronise")

def wait_for_CameraUpdated(sub_socket, camera_key, status):
    print("wait for: CameraUpdated {} {}", camera_key, status)
    while True:
        msg = wait_for(sub_socket, "CameraUpdated")
        if msg["CameraKey"] == camera_key and "CameraStatus" in msg and msg["CameraStatus"] == status:
            return msg

def wait_for_PhotoUpdated(sub_socket, camera_key, photo_key, location):
    print("wait for: PhotoUpdated {} {}", camera_key, photo_key, location)
    while True:
        msg = wait_for(sub_socket, "PhotoUpdated")
        if msg["CameraKey"] == camera_key and msg["PhotoLocation"] == location:
            if photo_key == "" or msg["PhotoKey"] == photo_key:
                return msg

def test(req_socket, sub_socket):
    send_synchronise(req_socket)
    msg = wait_for_Synchonise(sub_socket)
    camera_key = msg["CameraInfo"][0]["CameraKey"]
    send_connect(req_socket, camera_key)
    send_autofocus(req_socket, camera_key)
    wait_for_CameraUpdated(sub_socket, camera_key, "Busy")
    wait_for_CameraUpdated(sub_socket, camera_key, "Ready")
    send_setproperty(req_socket, camera_key, "Storage", "Card")
    send_shoot(req_socket, camera_key)
    wait_for_CameraUpdated(sub_socket, camera_key, "Busy")
    wait_for_CameraUpdated(sub_socket, camera_key, "Ready")
    msg = wait_for_PhotoUpdated(sub_socket, camera_key, "", "Camera")
    photo_key = msg["PhotoKey"]
    send_download(req_socket, photo_key)
    wait_for_CameraUpdated(sub_socket, camera_key, "Busy")
    wait_for_CameraUpdated(sub_socket, camera_key, "Ready")
    wait_for_PhotoUpdated(sub_socket, camera_key, photo_key, "Local Disk")

def main():
    parser = argparse.ArgumentParser("smartshooter-test.py")
    parser.add_argument("-l", "--loops",
                        type=int,
                        default=1,
                        metavar="NUM",
                        help="specify number of test loops to run")
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

    for i in range(args.loops):
        test(req_socket, sub_socket)

if __name__ == "__main__":
    main()
