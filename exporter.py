#!/usr/bin/env python3
import os
import http.server
import random

default_port = "9696"

port = int(os.environ.get('PORT', default_port))
current_value = 100


def get_stats() -> bytes:
    variance = random.randrange(-10, 10, 1)
    global current_value
    current_value = float(current_value + variance)

    return f"""#HELP test_exporter_metric simple test
#TYPE test_exporter_metric gauge
test_exporter_metric{{language="python"}} {current_value}""".encode('utf-8')


class Handler(http.server.SimpleHTTPRequestHandler):

    def metrics(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(get_stats())


    def do_GET(self):
        if self.path != "/metrics":
            self.send_error(404, message="unsupported endpoint")
            return

        self.metrics()


httpd = http.server.ThreadingHTTPServer(("0.0.0.0", port), Handler)
httpd.serve_forever()

