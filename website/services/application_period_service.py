from website import db
from website.models import ApplicationPeriod

class ApplicationPeriodService():
    def __init__(self, user_table, application_period_table):
        self.user_table = user_table
        self.application_period_table = application_period_table
    
    def getApplicationPeriodById(self, id: int):
        task = self.application_table.query.filter_by(id = id).first()
        print(task)
        return task

    def getApplicationPeriodsByDepartment(self, dep: str):
        application_periods = self.application_period_table.query.filter_by(deparment = dep).all()
        return application_periods