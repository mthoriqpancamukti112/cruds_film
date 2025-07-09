from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Admin
from . import db

auth_bp = Blueprint('auth', __name__)

# ROUTE HALAMAN LOGIN
@auth_bp.route('/login')
def login():
    """Route untuk menampilkan halaman login."""

    # Cek autentikasi
    if current_user.is_authenticated:
        # Jika user sudah login, alihkan ke halaman utama (frontend)
        return redirect(url_for('main.index'))
    
    # Jika belum login, tampilkan halaman login seperti biasa
    return render_template('auth/login.html')

# ROUTE LOGIN
@auth_bp.route('/login', methods=['POST'])
def login_post():
    """Route untuk memproses data login."""
    email = request.form.get('email')
    password = request.form.get('password')

    # Cari admin berdasarkan email
    admin = Admin.query.filter_by(email=email).first()

    # Cek apakah admin ada dan passwordnya cocok
    if not admin or not admin.verify_password(password):
        flash('Email atau password salah. Silakan coba lagi.', 'danger')
        return redirect(url_for('auth.login')) 

    # Jika berhasil, loginkan admin
    login_user(admin)
    return redirect(url_for('admin.dashboard'))

# ROUTE LOGOUT
@auth_bp.route('/logout')
@login_required
def logout():
    """Route untuk logout."""
    logout_user()
    return redirect(url_for('auth.login'))
