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

import sys
import json
import argparse
import zmq

def send_sequence_num(socket, sequence_num):
    req = {}
    req["msg_type"] = "Request"
    req["msg_id"] = "SetSequenceNumMsg"
    req["msg_ref_num"] = 0
    req['GridSequenceNum'] = sequence_num
    socket.send_string(json.dumps(req))
    rep = socket.recv()
    str_msg = rep.decode("utf-8")
    json_msg = json.loads(str_msg)
    return json_msg["Result"]

def send_batch_num(socket, batch_num):
    req = {}
    req["msg_type"] = "Request"
    req["msg_id"] = "SetBatchNumMsg"
    req["msg_ref_num"] = 0
    req['GridBatchNum'] = batch_num
    socket.send_string(json.dumps(req))
    rep = socket.recv()
    str_msg = rep.decode("utf-8")
    json_msg = json.loads(str_msg)
    return json_msg["Result"]

def send_unique_tag(socket, unique_tag):
    req = {}
    req["msg_type"] = "Request"
    req["msg_id"] = "SetOptionsMsg"
    req["msg_ref_num"] = 0
    req['GridUniqueTag'] = unique_tag
    socket.send_string(json.dumps(req))
    rep = socket.recv()
    str_msg = rep.decode("utf-8")
    json_msg = json.loads(str_msg)
    return json_msg["Result"]

def main():
    parser = argparse.ArgumentParser("smartshooter-setoptions.py [options]")
    parser.add_argument("-s", "--sequence",
                        type=int,
                        help="set the Sequence number")
    parser.add_argument("-b", "--batch",
                        type=int,
                        help="set the Batch number")
    parser.add_argument("-u", "--unique",
                        help="set the Unique Tag")
    parser.add_argument("-r", "--reqrep",
                        default="tcp://127.0.0.1:54544",
                        metavar="ENDPOINT",
                        help="specify ZMQ address of Smart Shooter request/reply server")
    args = parser.parse_args()

    context = zmq.Context()

    req_socket = context.socket(zmq.REQ)
    req_socket.connect(args.reqrep)

    if args.sequence != None:
        if not send_sequence_num(req_socket, args.sequence):
            print("Failed to send sequence number message", file=sys.stderr)
            exit(1)

    if args.batch != None:
        if not send_batch_num(req_socket, args.batch):
            print("Failed to send batch number message", file=sys.stderr)
            exit(1)

    if args.unique != None:
        if not send_unique_tag(req_socket, args.unique):
            print("Failed to send options message", file=sys.stderr)
            exit(1)

if __name__ == "__main__":
    main()
