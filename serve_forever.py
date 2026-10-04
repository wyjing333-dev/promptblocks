import http.server, socketserver, webbrowser, time, threading

PORT = 9999
DIRECTORY = r"D:\jieyuexingchen\promptblocks"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    def log_message(self, format, *args):
        pass  # silence logging

# Write a PID file so we know it's running
pid_file = r"D:\jieyuexingchen\promptblocks\server.pid"

import os
with open(pid_file, 'w') as f:
    f.write(str(os.getpid()))

print(f"PID {os.getpid()} written to {pid_file}")
print(f"Starting server on port {PORT}...")

def open_browser():
    time.sleep(1.5)
    webbrowser.open(f"http://localhost:{PORT}/")
    print("Browser opened.")

threading.Thread(target=open_browser, daemon=True).start()

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Serving {DIRECTORY} on http://localhost:{PORT}/")
    httpd.serve_forever()
