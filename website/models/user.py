from website import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    bilkent_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    role = db.relationship("Role", backref="user")     