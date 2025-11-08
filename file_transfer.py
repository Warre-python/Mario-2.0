import os
import socket
import struct

BUFFER_SIZE = 4096

def send_file(file_path, host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # Send metadata (filename length + filename + filesize)
    file_name_bytes = file_name.encode()
    client.send(struct.pack("!I", len(file_name_bytes)))  # filename length (4 bytes)
    client.send(file_name_bytes)
    client.send(struct.pack("!Q", file_size))  # file size (8 bytes)

    # Send file data
    with open(file_path, 'rb') as f:
        while chunk := f.read(BUFFER_SIZE):
            client.sendall(chunk)

    print(f"File '{file_name}' ({file_size} bytes) sent successfully.")
    client.close()


def receive_file(save_path, host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Listening on {host}:{port}...")

    conn, addr = server.accept()
    print(f"Connection from {addr} established.")

    # Receive metadata
    name_len = struct.unpack("!I", conn.recv(4))[0]
    file_name = conn.recv(name_len).decode()
    file_size = struct.unpack("!Q", conn.recv(8))[0]

    save_file_path = os.path.join(save_path, file_name)
    bytes_received = 0

    with open(save_file_path, 'wb') as f:
        while bytes_received < file_size:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            f.write(data)
            bytes_received += len(data)

    print(f"File '{file_name}' received successfully ({bytes_received} bytes).")

    conn.close()
    server.close()


if __name__ == "__main__":
    choice = input("Type 'send' to send a file or 'receive' to receive a file: ").strip().lower()
    if choice == 'send':
        file_path = input("Enter the path of the file to send: ").strip()
        host = input("Enter the receiver's IP address: ").strip()
        port = int(input("Enter the receiver's port number: ").strip())
        send_file(file_path, host, port)
    elif choice == 'receive':
        save_path = input("Enter the directory to save the received file: ").strip()
        host = input("Enter your IP address to listen on: ").strip()
        port = int(input("Enter the port number to listen on: ").strip())
        receive_file(save_path, host, port)
