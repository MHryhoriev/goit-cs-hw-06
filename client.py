from http.server import HTTPServer
from app.http_handler import HttpHandler
from app.config import HTTP_PORT

def run_http_server():
    """
    Starts an HTTP server that listens for incoming requests on the specified port.
    The server handles requests using the `HttpHandler` class.
    
    - Binds the server to the specified port.
    - Handles incoming HTTP requests indefinitely until interrupted.
    - Gracefully shuts down the server on a keyboard interrupt (Ctrl+C).
    """
    server_address = ('', HTTP_PORT)
    http = HTTPServer(server_address, HttpHandler)
    
    try:
        print(f'HTTP server started on port {HTTP_PORT}...')
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
        print('HTTP server stopped.')

if __name__ == "__main__":
    run_http_server()
