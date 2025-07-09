import os
from datetime import datetime
from flask import (
    Blueprint, render_template, request, 
    redirect, url_for, current_app, flash
)
from werkzeug.utils import secure_filename
from .models import Film, Admin
from . import db
from flask_login import login_required, current_user

# Membuat Blueprint baru bernama 'admin'
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ROUTE HALAMAN UTAMA DASHBOARD ATAU INDEX
@admin_bp.route('/')
@login_required # Amankan route ini
def dashboard():
     # Hitung total film dan admin
    total_films = Film.query.count()
    total_admins = Admin.query.count()
    return render_template(
        'dashboard/index.html', 
        total_films=total_films, 
        total_admins=total_admins
    )

# --- GRUP ROUTE FILM ---

# READ DATA FILM
@admin_bp.route('/data-film')
@login_required # Amankan route ini
def data_film():
    """Route untuk menampilkan halaman manajemen data film."""
    # Ambil semua data film, urutkan dari yang terbaru
    films = Film.query.order_by(Film.id.desc()).all()
    return render_template('dashboard/film/index.html', films=films)

# --- ROUTE PENCARIAN DATA FILM UNTUK ADMIN---
@admin_bp.route('/data-film/search', methods=['POST'])
@login_required
def search_admin_film():
    """Route untuk handle pencarian film di halaman admin via HTMX."""
    keyword = request.form.get('keyword')
    if keyword:
        films = Film.query.filter(Film.judul.ilike(f'%{keyword}%')).order_by(Film.id.desc()).all()
    else:
        films = Film.query.order_by(Film.id.desc()).all()
    # Render template parsial yang hanya berisi tabel
    return render_template('dashboard/film/_film_table.html', films=films)

# CREATE DATA FILM
@admin_bp.route('/data-film/tambah', methods=['GET', 'POST'])
@login_required # Amankan route ini
def tambah_film():
    """Route untuk menampilkan form dan memproses penambahan film."""
    if request.method == 'POST':
        # Ambil data dari form
        judul = request.form.get('judul')
        sutradara = request.form.get('sutradara')
        tahun_rilis = request.form.get('tahun_rilis')
        genre = request.form.get('genre')
        sinopsis = request.form.get('sinopsis')
        
        # Handle upload file gambar
        gambar = request.files.get('gambar')
        nama_file_gambar = None
        if gambar and gambar.filename != '':
            # Ambil ekstensi file asli (misal: .jpg, .png)
            _, f_ext = os.path.splitext(gambar.filename)
            # Amankan judul film untuk digunakan sebagai nama file
            judul_aman = secure_filename(judul)
            # Dapatkan timestamp
            timestamp = int(datetime.now().timestamp())
            # Gabungkan menjadi nama file baru yang unik
            nama_file_gambar = f"{timestamp}_{judul_aman}{f_ext}"
            path_simpan = os.path.join(current_app.config['UPLOAD_FOLDER'], nama_file_gambar)
            gambar.save(path_simpan)

        # Buat objek film baru dan simpan ke DB
        film_baru = Film(
            judul=judul,
            sutradara=sutradara,
            tahun_rilis=int(tahun_rilis),
            genre=genre,
            sinopsis=sinopsis,
            gambar=nama_file_gambar
        )
        db.session.add(film_baru)
        db.session.commit()
        
        # Alihkan ke halaman daftar film
        return redirect(url_for('admin.data_film'))

    # Jika method GET, tampilkan halaman form
    return render_template('dashboard/film/create.html')
pass

# EDIT DATA FILM
@admin_bp.route('/data-film/edit/<int:film_id>', methods=['GET', 'POST'])
@login_required # Amankan route ini
def edit_film(film_id):
    """Route untuk menampilkan form edit dan memproses update film."""
    film = Film.query.get_or_404(film_id)

    if request.method == 'POST':
        # Update data dari form
        judul_baru = request.form.get('judul')
        film.judul = judul_baru
        film.sutradara = request.form.get('sutradara')
        film.tahun_rilis = int(request.form.get('tahun_rilis'))
        film.genre = request.form.get('genre')
        film.sinopsis = request.form.get('sinopsis')

        # Handle jika ada gambar baru yang di-upload
        gambar_baru = request.files.get('gambar')
        if gambar_baru and gambar_baru.filename != '':
            # Hapus gambar lama jika ada untuk menghemat ruang
            if film.gambar:
                path_gambar_lama = os.path.join(current_app.config['UPLOAD_FOLDER'], film.gambar)
                if os.path.exists(path_gambar_lama):
                    os.remove(path_gambar_lama)
            
            # Simpan gambar baru
            _, f_ext = os.path.splitext(gambar_baru.filename)
            judul_aman = secure_filename(judul_baru)
            timestamp = int(datetime.now().timestamp())
            nama_file_gambar = f"{timestamp}_{judul_aman}{f_ext}"

            path_simpan = os.path.join(current_app.config['UPLOAD_FOLDER'], nama_file_gambar)
            gambar_baru.save(path_simpan)
            film.gambar = nama_file_gambar # Update nama file di DB

        db.session.commit()
        return redirect(url_for('admin.data_film'))

    # Jika method GET, tampilkan halaman form dengan data yang ada
    return render_template('dashboard/film/edit.html', film=film)
pass

# DELETE DATA FILM
@admin_bp.route('/data-film/hapus/<int:film_id>', methods=['POST'])
@login_required # Amankan route ini
def hapus_film(film_id):
    """Route untuk memproses penghapusan film."""
    # 1. Ambil data film dari database berdasarkan ID
    film = Film.query.get_or_404(film_id)
    
    # 2. Hapus file gambar terkait dari folder jika ada
    if film.gambar:
        path_gambar = os.path.join(current_app.config['UPLOAD_FOLDER'], film.gambar)
        if os.path.exists(path_gambar):
            os.remove(path_gambar)
            
    # 3. Hapus record film dari sesi database
    db.session.delete(film)
    
    # 4. Simpan perubahan (commit) ke database
    db.session.commit()
    
    # 5. Arahkan kembali ke halaman daftar film
    return redirect(url_for('admin.data_film'))
pass


# --- GRUP ROUTE ADMIN ---
# READ DATA ADMIN
@admin_bp.route('/data-admin')
@login_required
def data_admin():
    """Route untuk menampilkan daftar admin."""
    admins = Admin.query.order_by(Admin.id).all()
    return render_template('dashboard/admin/index.html', admins=admins)

# CREATE DATA ADMIN
@admin_bp.route('/data-admin/tambah', methods=['GET', 'POST'])
@login_required
def tambah_admin():
    """Route untuk menambah admin baru."""
    if request.method == 'POST':
        nama = request.form.get('nama')
        email = request.form.get('email')
        password = request.form.get('password')
        no_hp = request.form.get('no_hp')
        alamat = request.form.get('alamat')

        if not password:
            flash('Password wajib diisi.', 'danger')
            return redirect(url_for('admin.tambah_admin'))

        existing_admin = Admin.query.filter_by(email=email).first()
        if existing_admin:
            flash('Email sudah terdaftar. Silakan gunakan email lain.', 'danger')
            return redirect(url_for('admin.tambah_admin'))

        admin_baru = Admin(
            nama=nama,
            email=email,
            no_hp=no_hp,
            alamat=alamat
        )
        admin_baru.password = password
        db.session.add(admin_baru)
        db.session.commit()
        
        flash('Admin baru berhasil ditambahkan.', 'success')
        return redirect(url_for('admin.data_admin'))

    return render_template('dashboard/admin/create.html')

# EDIT DATA ADMIN
@admin_bp.route('/data-admin/edit/<int:admin_id>', methods=['GET', 'POST'])
@login_required
def edit_admin(admin_id):
    """Route untuk mengedit data admin."""
    admin = Admin.query.get_or_404(admin_id)
    if request.method == 'POST':
        admin.nama = request.form.get('nama')
        admin.email = request.form.get('email')
        admin.no_hp = request.form.get('no_hp')
        admin.alamat = request.form.get('alamat')
        
        password_baru = request.form.get('password')
        if password_baru:
            admin.password = password_baru
        
        db.session.commit()
        flash('Data admin berhasil diperbarui.', 'success')
        return redirect(url_for('admin.data_admin'))

    return render_template('dashboard/admin/edit.html', admin=admin)

# DELETE DATA ADMIN
@admin_bp.route('/data-admin/hapus/<int:admin_id>', methods=['POST'])
@login_required
def hapus_admin(admin_id):
    """Route untuk menghapus data admin."""
    # Mencegah admin menghapus akunnya sendiri
    if current_user.id == admin_id:
        flash('Anda tidak dapat menghapus akun Anda sendiri.', 'danger')
        return redirect(url_for('admin.data_admin'))

    admin_to_delete = Admin.query.get_or_404(admin_id)
    db.session.delete(admin_to_delete)
    db.session.commit()
    flash('Admin berhasil dihapus.', 'success')
    return redirect(url_for('admin.data_admin'))


