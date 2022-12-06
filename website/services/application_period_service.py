from website import db

class ApplicationPeriodService():
    def __init__(self, user_table, application_period_table):
        self.user_table = user_table
        self.application_period_table = application_period_table
    
    def getApplicationPeriodById(self, id: int):
        app = self.application_table.query.filter_by(id = id).first()
        return app

    def getApplicationPeriodsByDepartment(self, dep: str):
        application_periods = self.application_period_table.query.filter_by(department = dep).all()
        return application_periods