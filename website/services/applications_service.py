from website import db
class ApplicationsService():
    def __init__(self, user_table, application_table):
        self.user_table = user_table
        self.application_table = application_table
    
    def getApplicationById(self, id: int):
        task = self.application_table.query.filter_by(id = id).first()
        print(task)
        return task

    def getApplicationsByDepartment(self, dep: str):
        applications = self.application_table.query.filter_by(department = dep).all()
        return applications
    
    def getApplicationsByApplicationPeriodId(self, id: int):
        applications = self.application_table.query.filter_by(application_period_id = id).all()
        return applications