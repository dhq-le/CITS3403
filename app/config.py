import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_path = 'sqlite:///'+os.path.join(basedir, 'database.db')

class Config:
	SECRET_KEY = 'yoursecret-key'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../database.db') or default_database_path
	SQLALCHEMY_TRACK_MODIFICATIONS = False