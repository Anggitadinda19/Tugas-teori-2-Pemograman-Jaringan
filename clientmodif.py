import socket

def run_client():
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to server.")

        while True:
            user_input = input("Enter command: ")

            if user_input.lower() == 'exit':
                client_socket.sendall(user_input.encode('utf-8'))
                break

            if user_input.startswith("upload "):
                parts = user_input.split()
                if len(parts) < 3:
                    print("Usage: upload [file_name] [destination_dir]")
                    continue

                file_name = parts[1]
                destination_dir = parts[2]

                try:
                    client_socket.sendall(user_input.encode('utf-8'))

                    with open(file_name, 'rb') as file:
                        while chunk := file.read(1024):
                            client_socket.sendall(chunk)

                    print(f"File {file_name} sent to server.")
                except FileNotFoundError:
                    print(f"File {file_name} not found.")
            else:
                client_socket.sendall(user_input.encode('utf-8'))
                server_response = client_socket.recv(1024).decode('utf-8')
                print("Server response:", server_response)

if __name__ == "__main__":
    run_client()