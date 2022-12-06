from website import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """ User Table for Authentication """
    
    bilkent_id = db.Column(db.Integer, primary_key=True)
    
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    
    role = db.relationship("Role", backref="user")     
    applications = db.relationship("Applications", backref="user")     
    
    def get_id(self):
        return self.bilkent_id