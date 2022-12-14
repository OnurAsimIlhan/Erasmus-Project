from website import db

class Course(db.Model):
    """ Course Table for Authorization. One to Many Relationship with the University Table """
    
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50), nullable=False)
    equivalent_bilkent_course = db.Column(db.String(50), nullable=False)
    course_credit = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    syllabus = db.Column(db.LargeBinary)
    web_page = db.Column(db.String(50))
    approval_status = db.Column(db.String(50), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey("university.university_id"))
    course_coordinator = db.Column(db.Integer, db.ForeignKey("user.bilkent_id"))
    proposing_student = db.Column(db.Integer)
    is_elective = db.Column(db.Boolean, default=False, nullable=False)
    
    def get_id(self):
        return self.course_id