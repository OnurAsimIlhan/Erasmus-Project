from website import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """ User Table for Authentication """
    
    bilkent_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    role = db.relationship("Role", backref="user")
    courses = db.relationship("Course")     # course coordinator için 
    todo = db.relationship("Todo")  # course coordinator için 
    
    def get_id(self):
        return self.bilkent_id
