from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
from docx.shared import Mm
from io import BytesIO
import pythoncom
import os

from website import db


class PDFService:
    def __init__(self, application_table):
        self.application_table = application_table

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
        
    
    def create_preapproval_form(self):
        pass

    def sign_preapproval_form(self):
        pass

    def get_preapproval_form(self, id: int):
        pass