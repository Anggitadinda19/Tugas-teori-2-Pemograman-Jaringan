# Tugas-teori-2-pemograman-jaringan

# File Transfer Protocol menggunakan Socket Programming

## Nama: Anggita Rachmadinda Putri
## NIM: Nim 1203220086

### Penjelasan
Program ini adalah implementasi sederhana dari File Transfer Protocol (FTP) menggunakan socket programming dengan Python. FTP ini memungkinkan klien untuk berinteraksi dengan server menggunakan beberapa perintah, seperti:

- **ls**: Untuk menampilkan daftar file dan folder yang ada di server.
- **rm {nama_file}**: Untuk menghapus file dengan nama tertentu dari server.
- **Download {nama_file}**: Untuk mengunduh file dengan nama tertentu dari server.
- **Upload {nama_file}**: Untuk mengunggah file dengan nama tertentu ke server.
- **Size {nama_file}**: Untuk menampilkan informasi ukuran file dalam satuan MB dari file tertentu di server.
- **byebye**: Untuk memutuskan koneksi dengan server.
- **connme**: Untuk terhubung ke server.

### Cara Menggunakan
1. Jalankan `server.py` terlebih dahulu
2. Jalankan `client.py` untuk memulai klien dengan menjalankan perintah
3. Setelah klien terhubung, kita dapat memasukkan perintah-perintah berikut:
    - `ls`: Menampilkan daftar file dan folder di server.
    - `rm {nama_file}`: Menghapus file dengan nama tertentu dari server.
    - `Download {nama_file}`: Mengunduh file dengan nama tertentu dari server.
    - `Upload {nama_file}`: Mengunggah file dengan nama tertentu ke server.
    - `Size {nama_file}`: Menampilkan informasi ukuran file dalam satuan MB dari file tertentu di server.
    - `byebye`: Memutuskan koneksi dengan server.
    - `connme`: Terhubung kembali ke server.
