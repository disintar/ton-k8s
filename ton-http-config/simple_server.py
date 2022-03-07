from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import urlparse, parse_qs

current_wallet = 1


class SimpleServeFiles(BaseHTTPRequestHandler):
    def do_GET(self):
        global current_wallet
        o = urlparse(self.path)
        params = parse_qs(o.query)

        privelaged = False
        if 'token' in params and params['token'][0] == os.getenv('SHARED_SECRET'):
            privelaged = True

        files_to_share = ['config-local.json', 'config.json']
        if o.path[1:] in files_to_share:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            with open(f'/var/ton-work/network/{o.path[1:]}', 'r') as file:
                json_data = file.read()

                self.wfile.write(json_data.encode(encoding='utf_8'))
        elif privelaged and o.path == '/private':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write('true'.encode())
        elif o.path == '/wallet':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(f"{current_wallet}".encode())
            current_wallet += 1
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write("<h1>Hi</h1>".encode())


if __name__ == '__main__':
    simple_serve = HTTPServer(('0.0.0.0', int(os.getenv('PUBLIC_PORT'))), SimpleServeFiles)
    simple_serve.serve_forever()
