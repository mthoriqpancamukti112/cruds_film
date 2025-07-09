from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True akan membuat server otomatis restart saat ada perubahan kode
    # dan menampilkan pesan error yang lebih detail di browser.
    app.run(debug=True)