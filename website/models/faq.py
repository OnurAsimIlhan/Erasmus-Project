from website import db
import datetime

class Faq(db.Model):
    """ FAQ Table. FAQ's can be modified by Erasmus Coordinators """
    
    id = db.Column(db.Integer, primary_key=True)
    
    department = db.Column(db.String(5), nullable=False)
    question = db.Column(db.String(100), nullable=False, primary_key=True)
    answer = db.Column(db.String(100), nullable=False)