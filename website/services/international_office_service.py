from website import db
import pandas as pd
import io
from website.models import User


class InternationalOfficeService:
    
    def __init__(self, user_table, university_table, applications_table):
        self.user_table = user_table
        self.university_table = university_table
        self.applications_table = applications_table

    def getAppliedStudents(self, department:str):
        df = pd.DataFrame(columns=['FirstName', 'LastName', 'StudentID', 'Faculty', 'Department', 
                                    'Degree', 'CGPA'])
        applications = self.applications_table.query.all()
        for application in applications:
            student_id = application.student_id
            student = self.user_table.query.filter_by(bilkent_id = student_id).first()
            if student.department == department:
                name = student.name
                name_list = name.split()
                first_name = ' '.join(name_list[:-1])
                last_name = name_list[-1]
                new_row = {'FirstName': first_name, 'LastName': last_name, 'StudentID': student_id, 
                            'Faculty': 'Faculty of Engineering', 'Department': student.department, 
                            'Degree': 'undergraduate', 'CGPA': application.cgpa}
                df = df.append(new_row, ignore_index = True)

        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Applications')
        writer.save()
        output.seek(0)
        return output

    def place(self, department:str, file): # columns: StudentID | Score
        df = pd.read_excel(file)  
        sorted_df = df.sort_values(by=['Score'], ascending=False)
        for index in sorted_df.index:
            process_end = False
            application = self.applications_table.query.filter_by(student_id=sorted_df["StudentID"][index]).first()
            application.ranking = index

            student = self.user_table.query.filter_by(bilkent_id=sorted_df["StudentID"][index]).first()

            university_list = []
            university1 = self.university_table.query.filter_by(university_id = application.selected_university_1).first()
            university2 = self.university_table.query.filter_by(university_id = application.selected_university_2).first()
            university3 = self.university_table.query.filter_by(university_id = application.selected_university_3).first()
            university4 = self.university_table.query.filter_by(university_id = application.selected_university_4).first()
            university5 = self.university_table.query.filter_by(university_id = application.selected_university_5).first()
            university_list.append(university1)
            university_list.append(university2)
            university_list.append(university3)
            university_list.append(university4)
            university_list.append(university5)

            for university in university_list:
                if university != None and process_end == False:
                    for department in university.departments:
                        if department.department == student.department:
                            if department.remaining_quota > 0:
                                application.matched_university = university.university_id
                                department.remaining_quota = department.remaining_quota - 1
                                application.application_status = "Matched"
                                process_end = True
                else:
                    application.application_status = "WaitingList"
                    process_end = True
        db.session.commit() 

    def getDepartments(self):
        departments = []
        for department in db.session.query.distinct(User.name):
            departments.append(department)
        return departments


    

        
        
        
        
        
        
        
        
        
        
        
        
        
        