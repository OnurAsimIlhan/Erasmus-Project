import datetime

class FaqCreateRequest:
    def __init__(self, department, question, answer):
        self.department = department
        self.question = question
        self.answer = answer
        # self.date = datetime.datetime.now