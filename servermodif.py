import argparse
import os
import socket

def list_files(client_conn, dir_path='.'):
    try:
        items = os.listdir(dir_path)
        response = '\n'.join(items)
    except Exception as e:
        response = str(e)
    
    client_conn.sendall(response.encode('utf-8'))

def delete_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
        return f"File {filepath} successfully deleted."
    else:
        return f"File {filepath} does not exist."

def receive_file(client_conn, file_name, destination_dir='.'):
    try:
        destination_dir = os.path.abspath(destination_dir)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        file_path = os.path.join(destination_dir, file_name)

        # Check if file exists and create a new name if necessary
        original_file_path = file_path
        counter = 1
        while os.path.exists(file_path):
            file_base, file_ext = os.path.splitext(original_file_path)
            file_path = f"{file_base}_{counter}{file_ext}"
            counter += 1

        with open(file_path, 'wb') as file:
            while True:
                chunk = client_conn.recv(1024)
                if not chunk:
                    break
                file.write(chunk)

        file_size = os.path.getsize(file_path)
        return f"File {file_name} uploaded to {file_path} ({file_size} bytes)."
    except Exception as e:
        return f"Error uploading file {file_name}: {str(e)}"

def send_file(client_conn, file_name, source_dir='.'):
    try:
        source_dir = os.path.abspath(source_dir)
        file_path = os.path.join(source_dir, file_name)

        if not os.path.isfile(file_path):
            return f"File {file_name} does not exist in {source_dir}."

        with open(file_path, 'rb') as file:
            while chunk := file.read(1024):
                client_conn.sendall(chunk)

        file_size = os.path.getsize(file_path)
        return f"File {file_name} ({file_size} bytes) sent from {file_path}."
    except Exception as e:
        return f"Error downloading file {file_name}: {str(e)}"

def format_file_size(bytes_size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(bytes_size)
    unit = units.pop(0)

    while size > 1024 and units:
        size /= 1024
        unit = units.pop(0)

    return f"{size:.2f} {unit}"

def check_file_size(filepath):
    if os.path.isfile(filepath):
        size = os.path.getsize(filepath)
        return format_file_size(size)
    else:
        return f"File {filepath} does not exist."

def process_request(client_conn):
    while True:
        data = client_conn.recv(1024).decode('utf-8')
        if not data:
            break

        command = data.split()
        cmd = command[0]
        args = command[1:]

        if cmd == 'list':
            dir_path = args[0] if args else '.'
            list_files(client_conn, dir_path)
        elif cmd == 'delete':
            response = delete_file(args[0]) if args else "Usage: delete [file_path]"
            client_conn.sendall(response.encode('utf-8'))
        elif cmd == 'upload':
            if len(args) < 2:
                client_conn.sendall(b"Usage: upload [file_name] [destination_dir]")
            else:
                file_name = args[0]
                destination_dir = args[1]
                response = receive_file(client_conn, file_name, destination_dir)
                client_conn.sendall(response.encode('utf-8'))
        elif cmd == 'download':
            if len(args) < 1:
                client_conn.sendall(b"Usage: download [file_name]")
            else:
                file_name = args[0]
                response = send_file(client_conn, file_name)
                client_conn.sendall(response.encode('utf-8'))
        elif cmd == 'filesize':
            if len(args) < 1:
                client_conn.sendall(b"Usage: filesize [file_path]")
            else:
                filepath = args[0]
                response = check_file_size(filepath)
                client_conn.sendall(response.encode('utf-8'))
        elif cmd == 'disconnect':
            client_conn.sendall(b"Goodbye!")
            client_conn.close()
            break
        else:
            client_conn.sendall(b"Unknown command")

def start_server():
    HOST = '127.0.0.1'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server running on {HOST}:{PORT}")

        while True:
            client_conn, client_addr = server_socket.accept()
            print('Client connected:', client_addr)
            process_request(client_conn)

if __name__ == "__main__":
    start_server()