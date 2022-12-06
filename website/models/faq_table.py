from website import db

class faq_table(db.Model):
    """ University name and id table """
    #add question id
    question = db.Column(db.String(100), nullable=False, primary_key=True)
    answer = db.Column(db.String(100), nullable=False)
    
     