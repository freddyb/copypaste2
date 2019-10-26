#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
import marshal
import os
# import shlex
import signal
import subprocess
import sys
from time import sleep

database = {}


def signal_handler(signal, frame):
    print("\nApplication shutdown requested, writing database to disk...")
    json.dump(database, open("database.json", "w"))
    print("Done.")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

HTML_TEXT = open("index.html").read()


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
        self.wfile.write(HTML_TEXT.encode("utf-8"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            post_str = json.loads(post_data)
        except json.decoder.JSONDecodeError as e:
            post_str = {'cmd': ''}
        if post_str["cmd"] == "store":
            id = post_str['id']
            if id in database:
                database[id]["sanitized"] = post_str['vector']
                database[id]["fullhtml"] = post_str['raw']
            else:
                pass  # KOMISCH!!!! :-)

        elif post_str["cmd"] == "paste":
            start_pasting()
        self._set_headers()
        self.wfile.write(self._html("POST!"))


def run(server_class=ThreadingHTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


META_TAG = '<meta http-equiv="content-type" content="text/html; charset=utf-8">'


def make_rnd_id():
    return os.urandom(4).hex()


def paste():
    subprocess.run(["copyq", "paste"])


def copy(vector):
    h = str(hash(vector))
    combined = META_TAG + '0FREDMARKER' + h + 'FREDMARKER' + vector

    args = ["copyq", "copy", "text/html", combined]  # , "text/plain", i]
    database[h]["full"] = combined
    subprocess.run(args)


def make_simple_tag(tagname):
    return "<{}>hi</{}>".format(tagname, tagname)


def start_pasting():
    all = open("elements.txt", "r").read()

    for el in all.split("\n"):
        vector = make_simple_tag(el)
        h = str(hash(vector))
        database[h] = {"vector": vector, "elementname": el}
        copy(vector)
        paste()
        sleep(0.1)
    print("Done paste blasting :-)")


run()
