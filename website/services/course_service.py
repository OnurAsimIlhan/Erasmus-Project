from website import db
from website.models import User, Course
from io import BytesIO

class CourseService():
    def __init__(self, user_table, course_table, bilkent_course_table, university_table):
        self.user_table = user_table
        self.course_table = course_table
        self.bilkent_course_table = bilkent_course_table
        self.university_table = university_table

    def getBilkentCourseName(self, course_id : int):
        bilkent_course_name = self.bilkent_course_table.query.filter_by(course_id = course_id).first()
        return bilkent_course_name.course_name

    def getUniversityName(self, university_id : int):
        university = self.university_table.query.filter_by(university_id = university_id).first()
        return university.name

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
        