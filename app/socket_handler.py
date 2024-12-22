import socket
from datetime import datetime
import ast
from app.db import MongoDB

def handle_client(sock: socket.socket, address: str):
    """
    Handles communication with a connected client.
    Receives and processes data, inserts it into the database if valid.
    Responds back to the client after receiving the data.
    """
    print(f'Connection established with {address}')
    
    while True:
        received = sock.recv(1024)

        if not received:
            break
        try:
            data = ast.literal_eval(received.decode())
            if isinstance(data, dict):
                data_with_date = {'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}
                data_with_date.update(data)

                print(f'Data received: {data_with_date}')

                db = MongoDB()
                db.insert_message(data_with_date)
            else:
                print(f'Invalid data format: {data}')
        except (ValueError, SyntaxError) as ex:
            print(f'Error parsing data: {ex}')

        sock.send(b'Data received successfully')

    print(f'Connection closed with {address}')
    sock.close()

