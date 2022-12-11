from website import db
from website.dtos.applicationPeriodCreateRequest import ApplicationPeriodCreateRequest

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
    
    def addApplicationPeriod(self, application_period_create_request: ApplicationPeriodCreateRequest):
        application_period=self.application_period_table(
            department=application_period_create_request.department,
            deadline=application_period_create_request.deadline,
            status="Initial",
            type=application_period_create_request.type,
            title=application_period_create_request.title
        )
        db.session.add(application_period)
        db.session.commit()
        return application_period
        