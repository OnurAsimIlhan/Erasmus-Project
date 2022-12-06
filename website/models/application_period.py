from website import db

class ApplicationPeriod(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    applications = db.relationship("Applications")