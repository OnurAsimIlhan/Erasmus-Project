from website import db

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.bilkent_id"))
    
     