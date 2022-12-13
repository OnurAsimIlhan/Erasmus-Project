class UniversityService():
    def __init__(self, university_table, university_departments_table):
        self.university_table = university_table
        self.university_departments_table = university_departments_table
        
    def getAllUniversities(self):
        all_data = self.university_table.query.all()
        return all_data
    
    def getUniversitiesByDepartment(self, department: str):
        university_ids = self.university_departments_table.query.filter_by(department=department).all()
        
        universities = [self.university_table.query.filter_by(university_id=id.university_id).first() for id in university_ids]
            
        return universities
   
