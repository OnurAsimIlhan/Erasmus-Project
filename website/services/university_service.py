from website import db

class UniversityService():
    def __init__(self, university_table):
        self.university_table = university_table
        

    def getAllUniversities(self):
        all_data = self.university_table.query.all()
        return all_data

    def getUniversityById(self, id):
        university = self.university_table.query.filter_by(university_id = id).first()
        return university

    def getUniversitiesByDepartment(self, department):
        all_data = self.university_table.query.filter_by(departments = department).all()
        return all_data

    def addUniversity(self, name: str, country: str, semester: str, department: str, language: str, quota: int):
        new_university = self.university_table(
            name = name,
            country = country,
            semester = semester,
            departments = department,
            language_requirements = language,
            total_quota = quota,
            remaining_quota = quota
        )
        db.session.add(new_university)
        db.session.commit()
        return new_university

    def updateUniversity(self, id: int, name: str, country: str, semester: str, language: str, total_quota: int, remaining_quota: int):
        university = self.getUniversityById(id)
        university.name = name
        university.country = country
        university.semester = semester
        university.language_requirements = language
        university.total_quota = total_quota
        university.remaining_quota = remaining_quota
        db.session.commit()
        return university
    
    
   
