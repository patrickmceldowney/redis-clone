import socket
import threading
from datastore import Datastore


class RedisServer:
    def __init__(self, host='127.0.0.1', port=6379):
        self.host = host
        self.port = port
        self.datastore = Datastore()  # in-memory key/value store

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket: socket.socket):
        while True:
            try:
                request = client_socket.recv(1024).decode('utf-8')
                if not request:
                    break
                print(f"Received: {request}")

                response = self.process_request(request)
                client_socket.sendall(response.encode('utf-8'))
            except ConnectionResetError:
                print("Client connection disconnected abruptly")
                break

        client_socket.close()

    # Request should be formatted like COMMAND arg1 arg2
    def process_request(self, request: str) -> str:
        tokens = request.strip().split()
        if not tokens:
            return "ERROR: Empty command"

        command = tokens[0].upper()

        if command == 'SET' and len(tokens) == 3:
            key, value = tokens[1], tokens[2]
            self.datastore.set(key, value)
            return "OK"
        if command == 'GET' and len(tokens) == 2:
            key = tokens[1]
            value = self.datastore.get(key)
            if value is not None:
                return value
            else:
                return "NULL"
        else:
            return f"ERROR: Unknown or invalid command '{command}'"


# Run server
if __name__ == "__main__":
    server = RedisServer()
    server.start()
