import os

# Mendapatkan direktori dasar aplikasi
basedir = os.path.abspath(os.path.dirname(__file__))

# Menyimpan path ke folder instance
instance_dir = os.path.join(basedir, 'instance')
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(instance_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
