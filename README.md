# Tugas-teori-2-pemograman-jaringan File Transfer Protocol menggunakan Socket Programming

``` sh
Nama: Anggita Rachmadinda Putri
NIM: Nim 1203220086
```

# Penjelasan
Program ini adalah implementasi sederhana dari File Transfer Protocol (FTP) menggunakan socket programming dengan Python. FTP ini memungkinkan klien untuk berinteraksi dengan server menggunakan beberapa perintah, seperti:

- **ls**: Untuk menampilkan daftar file dan folder yang ada di server.
- **rm {nama_file}**: Untuk menghapus file dengan nama tertentu dari server.
- **Download {nama_file}**: Untuk mengunduh file dengan nama tertentu dari server.
- **Upload {nama_file}**: Untuk mengunggah file dengan nama tertentu ke server.
- **Size {nama_file}**: Untuk menampilkan informasi ukuran file dalam satuan MB dari file tertentu di server.
- **byebye**: Untuk memutuskan koneksi dengan server.
- **connme**: Untuk terhubung ke server.

## Source Code
1. File Server.py
```sh
import argparse
import os
import socket
```
Modul argparse dalam Python digunakan untuk menangani argumen baris perintah, membuat antarmuka baris perintah yang ramah pengguna, dan mempermudah pengelolaan argumen yang diteruskan ke skrip. Modul os berfungsi untuk berinteraksi dengan sistem operasi, menyediakan berbagai fungsi untuk operasi file dan direktori serta akses ke variabel lingkungan. Sementara itu, modul socket memungkinkan pengelolaan koneksi jaringan dan komunikasi melalui protokol jaringan, memungkinkan pembuatan dan pengelolaan koneksi jaringan tingkat rendah menggunakan protokol standar seperti TCP/IP. Ketiga modul ini sangat berguna dalam pengembangan skrip dan aplikasi Python yang memerlukan interaksi dengan lingkungan sistem operasi atau jaringan.

```sh
def list_files(client_conn, dir_path='.'):
    parser = argparse.ArgumentParser(description='List directory contents')
    parser.add_argument('dir_path', type=str, nargs='?', default='.')
    args = parser.parse_args()

    try:
        items = os.listdir(args.dir_path)
        response = '\n'.join(items)
    except Exception as e:
        response = str(e)
    
    client_conn.sendall(response.encode('utf-8'))
```
Fungsi list_files bertujuan untuk mengirim daftar isi dari sebuah direktori kepada klien yang terhubung melalui koneksi jaringan. Fungsi ini menerima dua parameter: client_conn, yang merupakan objek koneksi klien, dan dir_path, yang merupakan path dari direktori yang isinya akan didaftar, dengan default direktori saat ini (.). Pertama, fungsi menggunakan argparse untuk membuat parser argumen baris perintah dan menambahkan argumen dir_path. Kemudian, parser.parse_args() memparsing argumen yang diberikan di baris perintah dan menyimpannya dalam objek args. Selanjutnya, fungsi mencoba mendapatkan daftar item dalam direktori yang ditentukan oleh args.dir_path menggunakan os.listdir. Hasil dari os.listdir adalah daftar nama item dalam direktori, yang kemudian digabung menjadi satu string dengan pemisah newline (\n). Jika terjadi pengecualian, pesan error diubah menjadi string yang akan dijadikan respons. Akhirnya, fungsi mengirim string response yang telah di-encode ke dalam format UTF-8 melalui koneksi klien menggunakan client_conn.sendall(response.encode('utf-8')).

```sh
def delete_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
        return f"File {filepath} successfully deleted."
    else:
        return f"File {filepath} does not exist."
```
Fungsi delete_file dan receive_file masing-masing memiliki peran spesifik dalam mengelola file. Fungsi delete_file menerima sebuah parameter filepath dan mengecek apakah path yang diberikan menunjuk ke sebuah file yang ada menggunakan os.path.isfile. Jika file tersebut ada, fungsi akan menghapusnya dengan os.remove dan mengembalikan pesan bahwa file berhasil dihapus. Jika file tidak ada, fungsi akan mengembalikan pesan bahwa file tidak ditemukan.

```sh
def receive_file(client_conn, file_name, destination_dir='.'):
    try:
        destination_dir = os.path.abspath(destination_dir)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        file_path = os.path.join(destination_dir, file_name)

        if os.path.exists(file_path):
            overwrite = input(f"File {file_name} exists in {destination_dir}. Overwrite? (y/n): ")
            if overwrite.lower() != 'y':
                return f"Upload cancelled. File {file_name} not uploaded."

        with open(file_path, 'wb') as file:
            while True:
                chunk = client_conn.recv(1024)
                if not chunk:
                    break
                file.write(chunk)

        return f"File {file_name} uploaded to {file_path}."
    except Exception as e:
        return f"Error uploading file {file_name}: {str(e)}"
```
Fungsi receive_file bertugas menerima file dari klien yang terhubung dan menyimpannya di direktori tujuan yang ditentukan. Fungsi ini menerima tiga parameter: client_conn (koneksi klien), file_name (nama file yang akan diterima), dan destination_dir (direktori tujuan dengan default direktori saat ini). Fungsi mencoba mendapatkan path absolut dari direktori tujuan dan membuat direktori tersebut jika belum ada menggunakan os.makedirs. Selanjutnya, fungsi menggabungkan destination_dir dan file_name untuk mendapatkan file_path. Jika file dengan nama yang sama sudah ada di direktori tujuan, pengguna diminta konfirmasi untuk menimpa file tersebut. Jika pengguna memilih untuk tidak menimpa, fungsi akan membatalkan unggahan.

File kemudian dibuka dalam mode biner tulis ('wb') dan data diterima dalam potongan-potongan sebesar 1024 byte menggunakan client_conn.recv. Potongan data ini ditulis ke dalam file sampai semua data diterima. Setelah semua data diterima, fungsi mengembalikan pesan bahwa file berhasil diunggah ke lokasi tujuan. Jika terjadi kesalahan selama proses ini, pesan kesalahan yang dihasilkan akan dikembalikan.

```sh
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
```
Fungsi send_file bertugas untuk mengirimkan sebuah file dari server kepada klien melalui koneksi yang telah terhubung. Fungsi ini menerima tiga parameter: client_conn (koneksi klien), file_name (nama file yang akan dikirimkan), dan source_dir (direktori sumber dengan default direktori saat ini). Pertama, fungsi mencoba mendapatkan path absolut dari direktori sumber dan menggabungkan source_dir dan file_name untuk mendapatkan file_path. Jika file dengan nama tersebut tidak ditemukan di direktori sumber, fungsi akan mengembalikan pesan bahwa file tidak ada di direktori tersebut.

Jika file ada, fungsi membuka file tersebut dalam mode biner baca ('rb') dan membaca file dalam potongan-potongan sebesar 1024 byte. Setiap potongan data ini kemudian dikirimkan ke klien menggunakan client_conn.sendall. Setelah seluruh file berhasil dikirimkan, fungsi mendapatkan ukuran file menggunakan os.path.getsize dan mengembalikan pesan bahwa file telah berhasil dikirim dari path sumber beserta ukuran file dalam byte. Jika terjadi kesalahan selama proses ini, fungsi akan mengembalikan pesan kesalahan yang dihasilkan.

```sh
def format_file_size(bytes_size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(bytes_size)
    unit = units.pop(0)

    while size > 1024 and units:
        size /= 1024
        unit = units.pop(0)

    return f"{size:.2f} {unit}"
```
Fungsi format_file_size digunakan untuk mengonversi ukuran file dari byte ke format yang lebih mudah dibaca, seperti kilobyte (KB), megabyte (MB), gigabyte (GB), atau terabyte (TB). Fungsi ini menerima satu parameter, yaitu bytes_size, yang merupakan ukuran file dalam byte. Pertama, fungsi mendefinisikan daftar units yang berisi string untuk setiap unit ukuran yang mungkin: byte (B), kilobyte (KB), megabyte (MB), gigabyte (GB), dan terabyte (TB). Kemudian, fungsi mengonversi bytes_size menjadi tipe float dan menetapkan unit awal sebagai 'B'.

Selanjutnya, fungsi menggunakan loop while untuk membagi size dengan 1024 hingga nilainya kurang dari atau sama dengan 1024 atau tidak ada lagi unit yang tersisa di daftar units. Setiap kali size dibagi dengan 1024, unit berikutnya diambil dari daftar units menggunakan pop. Setelah loop selesai, fungsi mengembalikan ukuran file yang diformat dengan dua angka desimal, diikuti oleh unit yang sesuai. Misalnya, jika bytes_size adalah 1048576, fungsi akan mengembalikannya sebagai "1.00 MB".

```sh
def check_file_size(filepath):
    if os.path.isfile(filepath):
        size = os.path.getsize(filepath)
        return format_file_size(size)
    else:
        return f"File {filepath} does not exist."
```
Fungsi check_file_size bertujuan untuk memeriksa ukuran file pada filepath yang diberikan. Jika file tersebut ada, maka fungsi akan mengambil ukuran file menggunakan os.path.getsize(filepath). Ukuran tersebut kemudian akan diformat menggunakan fungsi format_file_size untuk mengonversinya menjadi format yang lebih mudah dibaca. Hasilnya akan dikembalikan sebagai string yang berisi ukuran file dalam format yang diinginkan. Jika file tidak ditemukan di filepath, fungsi akan mengembalikan pesan yang menyatakan bahwa file tersebut tidak ada.

```sh
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
            file_name = args[0] if args else ""
            destination_dir = input("Enter destination directory (leave blank for current directory): ")
            response = receive_file(client_conn, file_name, destination_dir)
            client_conn.sendall(response.encode('utf-8'))
        elif cmd == 'download':
            file_name = args[0] if args else ""
            response = send_file(client_conn, file_name)
            client_conn.sendall(response.encode('utf-8'))
        elif cmd == 'filesize':
            filepath = args[0] if args else ""
            response = check_file_size(filepath)
            client_conn.sendall(response.encode('utf-8'))
        elif cmd == 'disconnect':
            client_conn.sendall(b"Goodbye!")
            client_conn.close()
            break
        else:
            client_conn.sendall(b"Unknown command")
```
Fungsi process_request bertujuan untuk memproses permintaan yang diterima dari klien. Pada bagian awal, fungsi akan menerima data dari klien menggunakan client_conn.recv(1024). Data yang diterima kemudian di-decode menjadi string menggunakan utf-8. Selanjutnya, string data tersebut dipecah menjadi command dan argumen menggunakan split(). Command akan disimpan dalam variabel cmd, sedangkan argumen akan disimpan dalam list args.

Setelah itu, fungsi akan memeriksa command yang diterima. Jika command adalah 'list', fungsi akan memanggil list_files untuk menampilkan daftar file dalam direktori yang ditentukan. Jika command adalah 'delete', fungsi akan memanggil delete_file untuk menghapus file yang ditentukan. Jika command adalah 'upload', fungsi akan memanggil receive_file untuk menerima file dari klien. Jika command adalah 'download', fungsi akan memanggil send_file untuk mengirim file ke klien. Jika command adalah 'filesize', fungsi akan memanggil check_file_size untuk memeriksa ukuran file. Jika command adalah 'disconnect', fungsi akan mengirim pesan "Goodbye!" ke klien, menutup koneksi, dan keluar dari loop. Jika command tidak dikenali, fungsi akan mengirim pesan "Unknown command" ke klien.

```sh
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
```
Fungsi start_server bertujuan untuk memulai server pada alamat dan port tertentu. Pertama, host (HOST) dan port (PORT) ditentukan. Kemudian, server socket dibuat menggunakan socket.socket(socket.AF_INET, socket.SOCK_STREAM). Selanjutnya, server socket diikat ke alamat dan port yang telah ditentukan menggunakan bind((HOST, PORT)). Server kemudian siap menerima koneksi menggunakan listen(). Selama server berjalan, dalam loop while True, server akan menerima koneksi dari klien menggunakan accept(). Setelah koneksi diterima, server akan mencetak pesan bahwa klien telah terhubung. Selanjutnya, fungsi process_request akan dipanggil untuk memproses permintaan dari klien yang terhubung. Dengan demikian, fungsi start_server bertanggung jawab untuk memulai server, menerima koneksi dari klien, dan memproses permintaan klien menggunakan process_request.

```sh
if __name__ == "__main__":
    start_server()
```
Kode tersebut digunakan untuk memeriksa apakah file ini dijalankan sebagai program utama. Jika iya, start_server() akan dipanggil, memulai server.

2. File Client.py
```sh
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

            client_socket.sendall(user_input.encode('utf-8'))
            server_response = client_socket.recv(1024).decode('utf-8')
            print("Server response:", server_response)

if __name__ == "__main__":
    run_client()
```
Program di atas adalah klien sederhana yang berkomunikasi dengan server menggunakan protokol TCP/IP melalui socket. Pertama, kita menentukan host dan port server yang akan dihubungi. Kemudian, kita membuat objek socket klien dan menghubungkannya ke server menggunakan metode connect(). Selanjutnya, program memasuki loop tak terbatas dimana pengguna diminta untuk memasukkan perintah. Perintah tersebut dikirim ke server menggunakan sendall(), dan kemudian program menunggu respon dari server menggunakan recv(). Respon dari server kemudian dicetak ke layar. Jika pengguna memasukkan perintah "exit", program akan mengirim perintah tersebut ke server dan keluar dari loop, sehingga koneksi dengan server ditutup.

# Tugas Tambahan
1. Modifikasi agar file yang diterima dimasukkan ke folder tertentu 
2. Modifikasi program agar memberikan feedback nama file dan filesize yang diterima.
3. Apa yang terjadi jika pengirim mengirimkan file dengan nama yang sama dengan file yang telah dikirim sebelumnya? Dapat menyebabkan masalah kah ? Lalu bagaimana solusinya? Implementasikan ke dalam program, solusi yang Anda berikan.

## Server.py
Berikut adalah codingan setelah dimodifikasi agar sesuai dengan soal tambahan
``` sh
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
```
Perubahan:
Modifikasi Fungsi receive_file untuk Menentukan Direktori Tujuan dan Menangani Nama File yang Sama:
1. Penambahan argumen destination_dir.
2. Membuat direktori tujuan jika tidak ada.
3. Logika untuk menambahkan postfix angka jika file dengan nama yang sama sudah ada.
4. Memberikan feedback nama file dan ukuran file yang diterima.

Modifikasi Proses Permintaan untuk Perintah upload (pada fungsi upload):

```sh
elif cmd == 'upload':
    if len(args) < 2:
        client_conn.sendall(b"Usage: upload [file_name] [destination_dir]")
    else:
        file_name = args[0]
        destination_dir = args[1]
        response = receive_file(client_conn, file_name, destination_dir)
        client_conn.sendall(response.encode('utf-8'))
```
Perubahan:
Menambahkan penanganan untuk argumen destination_dir.

## Client.py
Berikut adalah codingan setelah dimodifikasi agar sesuai dengan soal tambahan
```sh
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
```
Perubahan:
Penanganan Perintah upload untuk Mengirim File ke Server dengan Direktori Tujuan:
1. Memastikan perintah upload memiliki format yang benar.
2. Mengirim file setelah memverifikasi perintah upload.
