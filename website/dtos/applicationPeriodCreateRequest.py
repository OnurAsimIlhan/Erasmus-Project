import datetime

class ApplicationPeriodCreateRequest:
    def __init__(self, department, title, type):
        self.department = department
        self.title = title
        self.type = type
        self.deadline = datetime.datetime.utcnow()