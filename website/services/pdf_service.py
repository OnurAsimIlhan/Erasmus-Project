from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
from docx.shared import Mm
from io import BytesIO
import pythoncom
import shutil
import os

from website import db


class PDFService:
    def __init__(self, application_table, university_table, course_table, bilkent_course_table, user_table):
        self.application_table = application_table
        self.university_table = university_table
        self.course_table = course_table
        self.bilkent_course_table = bilkent_course_table
        self.user_table = user_table

    def create_application_form(self, current_user, university_selections: list):
        document = DocxTemplate("forms/form_templates/application_form_template.docx")

        context = {
            "Name": current_user.name.split()[0],
            "Surname": current_user.name.split()[1],
            "ID": current_user.bilkent_id,
            "Department": current_user.department,
            "University1": university_selections[0] if university_selections[0] != None else "",
            "University2": university_selections[1] if university_selections[1] != None else "",
            "University3": university_selections[2] if university_selections[2] != None else "",
            "University4": university_selections[3] if university_selections[3] != None else "",
            "University5": university_selections[4] if university_selections[4] != None else "",
        }
        document.render(context)

        document.save("temp.docx")
        
        pythoncom.CoInitialize()
        convert(
            "temp.docx",
            "temp.pdf",
        )
        
        application = self.application_table.query.filter_by(student_id=current_user.bilkent_id).first()
        application.application_form = open("temp.pdf", "rb").read()
        db.session.commit()
        
        os.remove("temp.docx")
        os.remove("temp.pdf")

    def get_application_form(self, student_id: int):
        application = self.application_table.query.filter_by(student_id=student_id).first()
        file = BytesIO(application.application_form)
        
        return file
        
    def upload_application_form(self, student_id: int, file):
        application = self.application_table.query.filter_by(student_id=student_id).first()
        
        application.application_form = file.read()
        db.session.commit() 
        
    def create_preapproval_form(self, current_user, course_selections: list):
        document = DocxTemplate("forms/form_templates/pre_approval_form_template.docx")
        application = self.application_table.query.filter_by(student_id=current_user.bilkent_id).first()
        matched_university_id = application.matched_university
        matched_university = self.university_table.query.filter_by(university_id=matched_university_id).first()
        
        from datetime import date
        today = date.today()
        date = today.strftime("%d/%m/%Y")
        context = {
            "StudentName": current_user.name.split()[0],
            "StudentSurname": current_user.name.split()[1],
            "StudentID": current_user.bilkent_id,
            "StudentDepartment": current_user.department,
            "MatchedUniversity": matched_university.name,
            "CoordinatorName": "",
            "signature": "",
            "date": date,
        }
        
        i = 1
        for course_name in course_selections:
            if i == 11:
                break
            if course_name != None:
                course = self.course_table.query.filter_by(course_name=course_name,university_id=matched_university_id).first()
                bilkent_course = self.bilkent_course_table.query.filter_by(course_id=course.equivalent_bilkent_course).first()
                context[f"CourseName{i}"] = course_name
                context[f"CC{i}"] = course.course_id
                context[f"Credit{i}"] = course.course_credit
                context[f"BilkentCourse{i}"] = bilkent_course.course_name
                context[f"CB{i}"] = bilkent_course.course_credit
                context[f"Exemption{i}"] = ""
            else:
                context[f"CourseName{i}"] = ""
                context[f"CC{i}"] = ""
                context[f"Credit{i}"] = ""
                context[f"BilkentCourse{i}"] = ""
                context[f"CB{i}"] = ""
                context[f"Exemption{i}"] = ""
            i = i + 1
                
        document.render(context)
        document.save("temp.docx")
        pythoncom.CoInitialize()
        convert(
            "temp.docx",
            "temp.pdf",
        )

        application = self.application_table.query.filter_by(student_id=current_user.bilkent_id).first()
        application.pre_approval_form = open("temp.pdf", "rb").read()
        db.session.commit()
        os.remove("temp.docx")
        os.remove("temp.pdf")

    def sign_preapproval_form(self, coordinator_id: int, student_id: int):
        document = DocxTemplate("forms/form_templates/pre_approval_form_template.docx")
        username = self.user_table.query.filter_by(bilkent_id=coordinator_id).first().name
        path = f"forms/signatures/{username.split()[0].lower()}_{username.split()[1].lower()}_signature.png"
        
        context = {"signature": InlineImage(document, path, width=Mm(100), height=Mm(7))}
        
        document.render(context)
        
        document.save("temp.docx")
        pdf_path = f"forms/signed_forms/preapproval_form_{student_id}.pdf"
        
        pythoncom.CoInitialize()
        convert(
            "temp.docx",
            pdf_path,
        )
        
        application = self.application_table.query.filter_by(student_id=student_id).first()
        application.preapproval_form = None
        db.session.commit()
        
        os.remove("temp.docx")
        
    def get_preapproval_form(self, student_id: int):
        application = self.application_table.query.filter_by(student_id=student_id).first()
        if application.application_status == "waiting preapproval approval":
            file = BytesIO(application.preapproval_form)
        else:
            file = f"..\\forms\\signed_forms\\preapproval_form_{student_id}.pdf"
        
        return file
    
    def upload_application_form(self, student_id: int, file):
        application = self.application_table.query.filter_by(student_id=student_id).first()
        
        application.preapproval_form = file.read()
        db.session.commit() 
        
