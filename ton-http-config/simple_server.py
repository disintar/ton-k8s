from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class SimpleServeFiles(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/config.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            with open('/var/ton-work/network/config.json', 'r') as file:
                json_data = file.read()

                self.wfile.write(json_data.encode(encoding='utf_8'))
        else:
            self.send_response(404)


if __name__ == '__main__':
    simple_serve = HTTPServer(('0.0.0.0', int(os.getenv('PUBLIC_PORT'))), SimpleServeFiles)
    simple_serve.serve_forever()
