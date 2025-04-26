from flask import Flask

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yoursecret-key'

if __name__ == '__main__':
    application.run(debug=True)

#need to import app.routes 
import app.routes