from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import socket
import os
from app.config import TCP_IP, TCP_PORT, STATIC_DIR

class HttpHandler(BaseHTTPRequestHandler):
    """
    Handles HTTP GET and POST requests for a web application.
    This class serves dynamic HTML pages (like home and message pages), static files 
    (such as CSS and image files), and processes POST requests by sending data to a socket server.
    """

    def do_GET(self):
        """
        Handles GET requests.
        Routes the request to appropriate method based on the URL path.
        """
        pr_url = urllib.parse.urlparse(self.path)
        
        if pr_url.path == '/':
            self.handle_home_page()
        elif pr_url.path == '/message':
            self.handle_message_page()
        else:
            self.handle_static_files(pr_url)

    def handle_home_page(self):
        """
        Serves the home page (index.html).
        This page is returned when the user accesses the root URL ('/').
        """
        self.send_html_file('templates/index.html')

    def handle_message_page(self):
        """
        Serves the message page (message.html).
        This page is returned when the user accesses '/message'.
        """
        self.send_html_file('templates/message.html')

    def handle_static_files(self, pr_url):
        """
        Handles the serving of static files like CSS, images, etc.
        - Resolves the correct file path based on the URL.
        - If the file is found, it's sent back to the client.
        - If the file is not found, an error page is served instead.
        
        Args:
            pr_url: The parsed URL from the request, used to extract the file path.
        """
        file_path = os.path.join(STATIC_DIR, pr_url.path.lstrip('/'))
        
        if os.path.exists(file_path):
            self.send_static(file_path)
        else:
            self.send_html_file('templates/error.html', 404)

    def do_POST(self):
        """
        Handles POST requests.
        - Reads and parses the form data.
        - Sends the parsed data to a socket server for processing.
        - Redirects the user to the home page ('/').
        """
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}

        self.send_to_socket_server(data_dict)

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_to_socket_server(self, data_dict):
        """
        Sends the parsed data dictionary to a socket server for processing.
        - Establishes a socket connection to the server using TCP.
        - Sends the data and waits for a response from the server.
        - Prints the response from the socket server.
        
        Args:
            data_dict: The data dictionary to be sent to the socket server.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            server = (TCP_IP, TCP_PORT)
            sock.connect(server)
            print(f'Connected to socket server {server}')

            message = str(data_dict).encode()
            sock.send(message)

            response = sock.recv(1024)
            print(f'Socket server response: {response.decode()}')

    def send_html_file(self, filename, status=200):
        """
        Sends an HTML file as the HTTP response body.
        - Sets the content type to 'text/html'.
        - Sends the file to the client.
        
        Args:
        filename: The path to the HTML file to be served.
        status: The HTTP status code to be returned (default is 200 OK).
        """
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, file_path):
        """
        Sends a static file (e.g., CSS, images) as the HTTP response body.
        - Determines the MIME type of the file.
        - Sends the file to the client with the correct content type.
        
        Args:
        file_path: The path to the static file to be served.
        """
        self.send_response(200)
        mime_type, _ = mimetypes.guess_type(file_path)

        if mime_type:
            self.send_header('Content-type', mime_type)
        else:
            self.send_header('Content-type', 'application/octet-stream')
        self.end_headers()
        
        with open(file_path, 'rb') as file:
            self.wfile.write(file.read())
