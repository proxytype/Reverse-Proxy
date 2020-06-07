import http.server
import socketserver
import requests
import gzip
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import ssl


class ReverseProxy:
    class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
        parent = None

        def do_HEAD(self):
            pass

        def do_GET(self):
            return self.make_request()

        def do_POST(self):
            return self.make_request()

        def make_request(self):

            try:
                remote_headers = {}
                for header in self.headers:
                    header_value = self.headers[header]
                    header_value = header_value.replace(self.parent.source_address + ":" + str(self.parent.source_port),
                                                        self.parent.destination_address + ":" + str(
                                                            self.parent.destination_port))

                    remote_headers[header] = header_value

                url = 'https://{}{}'.format(self.parent.destination_address, self.path)

                if self.command == "GET":
                    r = requests.get(url, headers=remote_headers, verify=False)
                    self.send_response(r.status_code)
                    self.send_source_header(r)
                    self.wfile.write(r.content)

                if self.command == "POST":
                    length = int(self.headers["content-length"])
                    body = self.rfile.read(length)
                    r = requests.post(url, data=body, headers=remote_headers, verify=False)

                    self.send_response(r.status_code)
                    self.send_source_header(r)
                    self.wfile.write(r)

            except:
                pass
            finally:
                pass

        def send_source_header(self, response):

            response.headers["Access-Control-Allow-Origin"] = "*"

            for header in response.headers:
                if header not in ['Content-Encoding', 'content-encoding', 'Transfer-Encoding', 'transfer-encoding',
                                  'Content-Length', 'content-length']:
                    self.send_header(header, response.headers[header])

            self.send_header('Content-Length', len(response.content))

            self.end_headers()

    class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
        pass

    def __init__(self, _source_address, _source_port, _destination_address, _destination_port):
        self.source_address = _source_address
        self.source_port = _source_port
        self.destination_address = _destination_address
        self.destination_port = _destination_port

    def start_proxy(self):
        handler = self.MyRequestHandler
        handler.parent = self

        server = self.ThreadingSimpleServer(("", self.source_port), handler)
        try:
            print("serving at source port:", self.source_port)
            # server.socket = ssl.wrap_socket(server.socket, keyfile='./privkey.pem', certfile='./certificate.pem',
            #                                 server_side=True)
            server.serve_forever()
        except KeyboardInterrupt:
            pass
