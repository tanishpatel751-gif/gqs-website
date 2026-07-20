from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS 

app = Flask(__name__, 
            static_folder='../frontend/static', 
            static_url_path='/static', 
            template_folder='../frontend/templates')

# Secret key required for session and flashing
import os
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise RuntimeError('SECRET_KEY environment variable is required')

CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
from config import app, db 
with app.app_context():
    db.create_all()

# Import routes after creating app
from main import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
   
#ssl_context='adhoc' enables HTTPS for local development.
#This config.py file sets up the Flask application, 
# configures the database using SQLAlchemy, and enables CORS.