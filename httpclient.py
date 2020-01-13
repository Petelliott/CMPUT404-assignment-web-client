#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
import http404

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock

    def do_request(self, url, method, args=None, headers={}):
        body = None
        if args:
            body = urllib.parse.urlencode(args)
            headers["Content-Length"] = len(body)
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        urldata = urllib.parse.urlparse(url)

        if "Host" not in headers:
            # HTTP/1.1 requires a host header
            headers["Host"] = urldata.netloc

        with self.connect(urldata.hostname, urldata.port or 80) as sock:
            f = sock.makefile("rw")

            http404.Request(urldata.path, method, headers, body).write_to(f)

            # shutdown writing, our client does not support persistant
            # connections
            sock.shutdown(socket.SHUT_WR)
            r = http404.Response.read_from(f)
            return HTTPResponse(r.statusn, r.body.read())


    def GET(self, url, args=None):
        return self.do_request(url, "GET", args)

    def POST(self, url, args=None):
        return self.do_request(url, "POST", args)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
