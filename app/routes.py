from flask import Blueprint, render_template, request
from .models import Film  # Impor model Film

main = Blueprint('main', __name__)

# ROUTE UTAMA ATAU HOME
@main.route('/')
def index():
    """Route untuk halaman utama (katalog film)."""
    # Ambil semua data film dari database
    semua_film = Film.query.order_by(Film.tahun_rilis.desc()).all()
    # Render template halaman utama dan kirim data film
    return render_template('home/index.html', films=semua_film)

# ROUTE PENCARIAN PADA HALAMAN HOME
@main.route('/cari-film', methods=['POST'])
def cari_film():
    """Route untuk handle pencarian film via HTMX."""
    keyword = request.form.get('keyword')
    
    if keyword:
        # Cari film berdasarkan judul (case-insensitive)
        hasil = Film.query.filter(Film.judul.ilike(f'%{keyword}%')).order_by(Film.tahun_rilis.desc()).all()
    else:
        # Jika keyword kosong, tampilkan semua film
        hasil = Film.query.order_by(Film.tahun_rilis.desc()).all()
        
    # Render template parsial dan kembalikan hanya HTML kartu filmnya
    return render_template('home/_film_cards.html', films=hasil)