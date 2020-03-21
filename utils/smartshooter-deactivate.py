#!/usr/bin/env python3
#
# Copyright (c) 2020, Kuvacode Oy. All rights reserved.
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

def send_deactivate(socket):
    req = {}
    req["msg_type"] = "Request"
    req["msg_id"] = "DeactivateLicense"
    req["msg_seq_num"] = 10
    socket.send_string(json.dumps(req))
    rep = socket.recv()
    str_msg = rep.decode("utf-8")
    json_msg = json.loads(str_msg)
    return json_msg["msg_result"]

def main():
    parser = argparse.ArgumentParser("smartshooter-deactivate.py")
    parser.add_argument("-r", "--reqrep",
                        default="tcp://127.0.0.1:54544",
                        metavar="ENDPOINT",
                        help="specify ZMQ address of Smart Shooter request/reply server")
    args = parser.parse_args()

    context = zmq.Context()

    req_socket = context.socket(zmq.REQ)
    req_socket.connect(args.reqrep)

    if send_deactivate(req_socket):
        print("License deactivated")
    else:
        print("Failed to deactivate license", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()
