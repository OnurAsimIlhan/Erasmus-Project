from website import db

class Deadlines(db.Model):
    """ Deadlines Table. Deadlines can be set by Erasmus Coordinators """
    
    id = db.Column(db.Integer, primary_key=True)
    
    mission = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    
    