import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_path = 'sqlite:///'+os.path.join(basedir, 'database.db')

class Config:
	SECRET_KEY = 'yoursecret-key'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', default_database_path)