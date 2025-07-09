import os

# Dapatkan path absolut dari direktori aplikasi
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci-rahasia-yang-sangat-sulit-ditebak'
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/db_film'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')