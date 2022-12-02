from website import db

class University(db.Model):
    """ placeholder university table """
    university_id = db.Column(db.Integer, primary_key=True)
