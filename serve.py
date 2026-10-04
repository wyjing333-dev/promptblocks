import http.server, socketserver, threading, webbrowser, time

PORT = 8765
DIRECTORY = r"D:\jieyuexingchen\promptblocks"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving on http://localhost:{PORT}/")
        httpd.serve_forever()

# Start server in background thread
t = threading.Thread(target=start_server, daemon=False)
t.daemon = True
t.start()

# Wait a moment then open browser
time.sleep(1)
webbrowser.open(f"http://localhost:{PORT}/")
print("Browser opened. Press Ctrl+C to stop server.")
# Keep main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Server stopped.")
