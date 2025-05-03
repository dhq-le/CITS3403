import os
# the single place where you read and write any setting that your application or its extensions need.

basedi = os.path.abspath(os.path.dirname(__file__))
default_database_path = 'sqlite:///'+os.path.join(basedi, 'app.db')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or default_database_path   
    # It is better to use environment variables for the databas URL. 
