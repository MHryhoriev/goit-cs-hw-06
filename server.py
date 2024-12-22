import socket
from app.config import TCP_IP, TCP_PORT
from app.socket_handler import handle_client

def run_socket_server():
    """
    Starts a TCP socket server that listens on the specified IP and port.
    It accepts incoming client connections and handles them.
    The server runs until interrupted.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_IP, TCP_PORT))
    server_socket.listen(10)
    print(f'Socket server started at {TCP_IP}:{TCP_PORT}')
    try:
        while True:
            new_sock, address = server_socket.accept()
            handle_client(new_sock, address)
    except KeyboardInterrupt:
        print('Shutting down the socket server.')
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_socket_server()
