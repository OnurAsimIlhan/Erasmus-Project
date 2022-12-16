"""from website import db
from website.dtos.applicationPeriodCreateRequest import ApplicationPeriodCreateRequest
from website.dtos.applicationPeriodUpdateRequest import ApplicationPeriodUpdateRequest

class ApplicationPeriodService():
    def __init__(self, user_table, application_period_table):
        self.user_table = user_table
        self.application_period_table = application_period_table
        self.STATUS_LIST = [
            "Initialized", 
            "Application", 
            "Placement", 
            "Preapproval", 
            "Mobilization", 
            "Course-Transfer", 
            "Completed"
        ]
        self.TYPE_LIST = {
            "Erasmus",
            "Exchange"
        }
    
    def getApplicationPeriodById(self, id: int):
        app = self.application_period_table.query.filter_by(id = id).first()
        return app

    def getApplicationPeriodsByDepartment(self, dep: str):
        application_periods = self.application_period_table.query.filter_by(department = dep).all()
        return application_periods
    
    def addApplicationPeriod(self, application_period_create_request: ApplicationPeriodCreateRequest):
        application_period=self.application_period_table(
            department=application_period_create_request.department,
            deadline=application_period_create_request.deadline,
            status=self.STATUS_LIST[0],
            type=application_period_create_request.type,
            title=application_period_create_request.title
        )
        db.session.add(application_period)
        db.session.commit()
        return application_period
    
    def updateApplicationPeriod(self, id, application_period_create_request: ApplicationPeriodUpdateRequest):
        application_period = self.application_period_table.query.filter_by(id=id).first()

        if application_period == None:
            return None
        else:
            application_period.title=application_period_create_request.title
            application_period.status=application_period_create_request.status
            print(application_period_create_request.status)
            if application_period_create_request.deadline != None:
                application_period.deadline=application_period_create_request.deadline
            
            db.session.commit()
            return application_period
    
    def deleteApplicationPeriod(self, id):
        application_period = self.application_period_table.query.filter_by(id = id).first()
        db.session.delete(application_period)
        db.session.commit()
    
    def terminateApplicationPeriod(self, id):
        application_period = self.application_period_table.query.filter_by(id = id).first()
        if application_period != None:
            application_period.status = self.STATUS_LIST[-1]
            db.session.commit()
        
        return application_period

        """