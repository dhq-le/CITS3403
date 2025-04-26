from flask import Flask

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yoursecret-key'

#need to import app.routes 
from app import routes