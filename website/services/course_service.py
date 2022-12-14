from website import db
from website.models import User, Course
from io import BytesIO

class CourseService():
    def __init__(self, user_table, course_table):
        self.user_table = user_table
        self.course_table = course_table
    
    def approveCourse(self, course_id : int):
        course = self.course_table.query.filter_by(course_id = course_id).first()
        course.approval_status = "Approved"
        db.session.commit()
    def rejectCourse(self, course_id : int):
        course = self.course_table.query.filter_by(course_id = course_id).first()
        course.approval_status = "Rejected"
        db.session.commit()

    def sendSyllabus(self, course_id : int):
        course = self.course_table.query.filter_by(course_id = course_id).first()
        file = BytesIO(course.syllabus) 
        return file
        