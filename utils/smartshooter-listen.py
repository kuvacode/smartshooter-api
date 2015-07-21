#!/usr/bin/env python
#
# Copyright (c) 2015, Kuvacode Oy. All rights reserved.
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
import datetime
import argparse
import zmq

def main():
    parser = argparse.ArgumentParser("smartshooter-listen.py")
    parser.add_argument("-q", "--quiet",
                        action="store_true",
                        default=False,
                        help="enable quiet mode for reduced logging")
    parser.add_argument("-p", "--publisher",
                        default="tcp://127.0.0.1:54543",
                        metavar="ENDPOINT",
                        help="specify ZMQ address of Smart Shooter publisher")
    args = parser.parse_args()

    context = zmq.Context()

    sub_socket = context.socket(zmq.SUB)
    sub_socket.setsockopt(zmq.SUBSCRIBE, b"")
    sub_socket.connect(args.publisher)

    while (True):
        raw = sub_socket.recv()
        str_msg = raw.decode("utf-8")
        json_msg = json.loads(str_msg)
        print("{0}: {1}".format(datetime.datetime.now(), json_msg["msg_id"]))
        if not args.quiet:
            print(str_msg)

if __name__ == "__main__":
    main()
