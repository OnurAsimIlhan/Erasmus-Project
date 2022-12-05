import datetime

class FaqUpdateRequest:
    def __init__(self, department, info):
        self.department = department
        self.info = info
        # self.date = datetime.datetime.now