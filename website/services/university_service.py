class UniversityService():
    def __init__(self, university_table):
        self.university_table = university_table
        

    def getAllUniversities(self):
        all_data = self.university_table.query.all()
        return all_data
    
   