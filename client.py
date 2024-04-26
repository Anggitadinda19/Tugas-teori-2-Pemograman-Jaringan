import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    print("Koneksi berhasil. Ketik 'connme' untuk masuk ke dalam server.")

    while True:
        command = input("Command: ")

        client_socket.sendall(command.encode())
        response = client_socket.recv(1024).decode()

        if response == "disconnect":
            print("Server memutus koneksi.")
            break
        elif response.startswith("File"):
            print(response)
            continue
        elif response.startswith("Ukuran"):
            print(response)
            continue
        elif response.startswith("Koneksi"):
            print(response)
            continue

        print(response)

    client_socket.close()

if __name__ == "__main__":
    main()