#!/usr/bin/env python3
import json
import os
import shlex
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("hi!"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_str = json.loads(post_data)
        print("posted", post_str)

        self._set_headers()
        self.wfile.write(self._html("POST!"))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


META_TAG = '<meta http-equiv="content-type" content="text/html; charset=utf-8">'


def make_rnd_id():
    return os.urandom(2).hex()


def paste():
    subprocess.run(["copyq", "paste"])


def copy(vector):
    i = make_rnd_id()
    combined = META_TAG + '\n' + i + '\nFREDMARKER\n' + vector
    args = ["copyq", "copy", "text/html", combined]  # , "text/plain", i]

    print(args)
    print(subprocess.run(args))


def make_simple_tag(tagname):
    return "<{}>hi</{}>".format(tagname, tagname)


for el in ["a", "b", "c", "d", "em", "k", "i", "l", "q", "s"]:
    h = make_simple_tag(el)
    print(h)
# copy(h)
# paste()

run()

"""


sleep 1
copyq copy text/html '<meta http-equiv="content-type" content="text/html; charset=utf-8"><b id="a">l0rn</b>'
sleep 1; copyq paste
copyq copy text/html '<meta http-equiv="content-type" content="text/html; charset=utf-8"><a id="b">l0rn</a>'
sleep 1; copyq paste
copyq copy text/html '<meta http-equiv="content-type" content="text/html; charset=utf-8"><i id="c">l0rn</i>'
sleep 1; copyq paste
copyq copy text/html '<meta http-equiv="content-type" content="text/html; charset=utf-8"><s id="e">l0rn</s>'
sleep 1; copyq paste
copyq copy text/html '<meta http-equiv="content-type" content="text/html; charset=utf-8"><em id="d">l0rn</em>'
sleep 1; copyq paste

"""
