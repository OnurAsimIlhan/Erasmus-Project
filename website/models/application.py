from website import db

class Application(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    deparment = db.Column(db.String(5), nullable=False)
    info = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("user.bilkent_id"))
    application_period_id = db.Column(db.Integer, db.ForeignKey("application_period.id"))