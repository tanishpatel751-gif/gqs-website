from config import db 

class Product(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(120)) 
    name = db.Column(db.String(80), unique=True, nullable=False) 
    descript = db.Column(db.String(120), nullable=False)
    price= db.Column(db.Float, nullable=False)