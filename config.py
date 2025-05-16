import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_path = 'sqlite:///'+os.path.join(basedir, 'database.db')

load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Fallback option if SECRET_KEY is not set in .env:
    # SECRET_KEY = os.environ.get('SECRET_KEY', 'default-fallback-secret')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', default_database_path)

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    # Use an in-memory SQLite database for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False