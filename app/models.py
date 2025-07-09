from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # Import UserMixin

class Film(db.Model):
    """Model untuk tabel film di database."""
    
    __tablename__ = 'film'

    id = db.Column(db.Integer, primary_key=True)
    gambar = db.Column(db.String(255), nullable=True) 
    judul = db.Column(db.String(150), nullable=False)
    sutradara = db.Column(db.String(100), nullable=False)
    tahun_rilis = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=True)
    sinopsis = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Film {self.judul}>'

class Admin(UserMixin, db.Model):
    """Model untuk tabel admin."""
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    no_hp = db.Column(db.String(20), nullable=True)
    alamat = db.Column(db.Text, nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Method untuk men-set dan meng-hash password."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Method untuk memverifikasi password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.nama}>'