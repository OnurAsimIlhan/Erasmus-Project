from website import db
import datetime

class Faq(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(5), nullable=False)
    info = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime)