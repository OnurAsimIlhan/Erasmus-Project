from website import db


class Form(db.Model):
    formID = db.Column(db.Integer, primary_key=True)
    approvalStatus = db.Column(db.String(50), nullable=False)
    studentID = db.Column(db.Integer, db.ForeignKey("user.bilkent_id"))
