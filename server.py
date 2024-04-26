import socket

def hitung_jumlah_karakter(pesan):
    return str(len(pesan))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

print("Server berjalan. Menunggu koneksi...")

while True:
    client_socket, client_address = server_socket.accept()
    print("Terhubung dengan", client_address)

    pesan_dari_klien = client_socket.recv(1024).decode()

    if pesan_dari_klien:
        print("Pesan dari klien:", pesan_dari_klien)
        
        jumlah_karakter = hitung_jumlah_karakter(pesan_dari_klien)

        client_socket.send(jumlah_karakter.encode())
        print("Jumlah karakter pesan:", jumlah_karakter)

    client_socket.close()