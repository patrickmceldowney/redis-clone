import socket


def send_command(command: str):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 6379))
    client_socket.sendall(command.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Response: {response}")

    client_socket.close()


if __name__ == "__main__":
    send_command("SET mykey myvalue")
    send_command("GET mykey")
