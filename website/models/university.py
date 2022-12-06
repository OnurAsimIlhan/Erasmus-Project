from website import db

class University(db.Model):
    """ University name and id table """

    university_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    

    def __repr__(self):
        return f'<Name {self.name}>'
     