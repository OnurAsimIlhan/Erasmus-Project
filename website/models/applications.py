from website import db

class Applications(db.Model):
    """ Applications Table that tracks the application process of all students """
    
    application_id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey("user.bilkent_id"))
    #matched_university = db.Column(db.Integer, db.ForeignKey("university.university_id"), nullable=True)
    #selected_university_1 = db.Column(db.Integer, db.ForeignKey("university.university_id"), nullable=True)
    #selected_university_2 = db.Column(db.Integer, db.ForeignKey("university.university_id"), nullable=True)
    #selected_university_3 = db.Column(db.Integer, db.ForeignKey("university.university_id"), nullable=True)
    #selected_university_4 = db.Column(db.Integer, db.ForeignKey("university.university_id"), nullable=True)
    #selected_university_5 = db.Column(db.Integer, db.ForeignKey("university.university_id"), nullable=True)
        
    department = db.Column(db.String(10), nullable=False)
    cgpa = db.Column(db.Integer, nullable=False)
    application_status = db.Column(db.String(50), nullable=False)
    ranking = db.Column(db.Integer, nullable=True)
    erasmus_points = db.Column(db.Integer, nullable=True)
    
    application_form = db.Column(db.String(100), nullable=True)
    pre_approval_form = db.Column(db.String(100), nullable=True)
    learning_agreement_form = db.Column(db.String(100), nullable=True)