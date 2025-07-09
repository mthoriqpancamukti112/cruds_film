Panduan Instalasi Aplikasi FilmKu

Langkah 1: Persiapan Awal (Prasyarat)
Pastikan perangkat lunak berikut sudah terinstal di laptop teman Anda:
1. Python: Pastikan Python sudah terinstal. Anda bisa cek dengan membuka terminal dan mengetik:
   - python --version.
3. Git: Diperlukan untuk mengunduh proyek dari GitHub.
4. Laragon: Sebagai server lokal dan database MySQL.

Langkah 2: Unduh Proyek dari GitHub
1. Buka Terminal atau Command Prompt.
2. Arahkan ke direktori tempat Anda ingin menyimpan proyek (misalnya, Documents atau Projects)
3. Jalankan perintah git clone dengan URL repositori GitHub Anda.
   - git clone https://github.com/nama-anda/nama-repositori-anda.git
4. Masuk ke dalam folder proyek yang baru saja diunduh.
   - cd nama-folder

Langkah 3: Siapkan Lingkungan Virtual & Instal Pustaka
Ini adalah langkah paling penting untuk mengisolasi proyek.
1. Buat Virtual Environment: Di dalam folder proyek, jalankan:
   - python -m venv venv
2. Aktifkan Virtual Environment:
   - Windows: venv\Scripts\activate
   - macOS/Linux: source venv/bin/activate
     (Terminal akan menampilkan (venv) di awal baris).
3. Instal Semua Pustaka: Gunakan file requirements.txt untuk menginstal semua yang dibutuhkan dengan satu perintah.
   - pip install -r requirements.txt

Langkah 4: Siapkan Database
1. Jalankan Laragon: Buka aplikasi Laragon dan klik "Start All" untuk menjalankan Apache dan MySQL.
2. Buat Database:
   - Klik tombol "Database" di Laragon untuk membuka HeidiSQL.
   - Di HeidiSQL, klik kanan pada area kosong di panel kiri, pilih "Create new" -> "Database".
   - Beri nama database db_film (harus sama persis dengan yang ada di config.py). Lalu klik OK.

Langkah 5: Buat Tabel di Database
Sekarang kita akan membuat tabel film dan admin berdasarkan model yang ada di kode.
1. Pastikan terminal Anda masih di dalam folder proyek dengan (venv) aktif.
2. Jalankan Flask Shell:
   - flask shell
3. Setelah masuk ke shell (>>>), jalankan dua perintah ini:
   - from app import db
  -  db.create_all()
   Perintah ini akan membuat semua tabel. Setelah selesai, keluar dari shell dengan mengetik exit().

Langkah 6: Buat Akun Admin Pertama
Database masih kosong, jadi teman Anda tidak akan bisa login. Buat satu akun admin pertama melalui shell.
1. Jalankan lagi flask shell.
   - flask shell
2. Jalankan perintah Python berikut untuk membuat admin:
   - from app.models import Admin
   - from app import db
   - admin_baru = Admin(email='admin@gmail.com', nama='Admin Film', password='12345')
   - db.session.add(admin_baru)
   - db.session.commit()
   - exit()

Langkah 7: Jalankan Aplikasi!
Ini adalah langkah terakhir.
1. Di terminal (dengan (venv) aktif), jalankan perintah:
   - python run.py
2. Buka browser dan kunjungi alamat http://127.0.0.1:5000.

Aplikasi sekarang seharusnya sudah berjalan dengan baik :)
