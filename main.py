import multiprocessing
from server import run_socket_server
from client import run_http_server

def start_socket_server():
    run_socket_server()

def start_http_server():
    run_http_server()

def main():
    socket_process = multiprocessing.Process(target=start_socket_server)
    http_process = multiprocessing.Process(target=start_http_server)

    socket_process.start()
    http_process.start()
    
    socket_process.join()
    http_process.join()

if __name__ == '__main__':
    main()
