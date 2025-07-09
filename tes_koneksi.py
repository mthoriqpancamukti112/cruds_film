import pymysql

# --- Atur Detail Koneksi ---
host = 'localhost'
user = 'root'
password = ''
db = 'db_film'
# -----------------------------------------

try:
    # Coba buat koneksi ke database
    koneksi = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        connect_timeout=5  # Timeout setelah 5 detik jika gagal
    )
    
    print("Koneksi Berhasil!")
    print(f"Terhubung ke database '{db}' di host '{host}'")
    
    # Tutup koneksi setelah selesai
    koneksi.close()

except pymysql.Error as e:
    # Tangkap dan tampilkan pesan error jika koneksi gagal
    print(f"KONEKSI GAGAL. Error: {e}")