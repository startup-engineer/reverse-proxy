from http import server
import requests

cluster = [
    'http://localhost:8001',
    'http://localhost:8002',
]

last_used = 0
def get_server():
    global last_used
    last_used = (last_used + 1) % len(cluster)
    return cluster[last_used]

class ProxyHTTPRequestHandler(server.BaseHTTPRequestHandler):    
    def do_GET(self):
        request_headers = self.headers
        proxied_host = get_server()

        response = requests.get(proxied_host, headers=request_headers)

        self.send_response(response.status_code)
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.content)        

server_address = ('', 8000)
httpd = server.HTTPServer(server_address, ProxyHTTPRequestHandler)
httpd.serve_forever()