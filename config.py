import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_path = 'sqlite:///'+os.path.join(basedir, 'database.db')

class Config:
	SECRET_KEY = 'fhfuw9eg8eu3oievjeopfijvdfpovjefujhevofjevpoiefwhv'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', default_database_path)


class TestConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # Use a separate test database