from .singleton import Singleton

from website.dtos.faqCreateRequest import FaqCreateRequest
from website.dtos.faqUpdateRequest import FaqUpdateRequest
import datetime

from website import db
class FaqService(metaclass=Singleton):
    def __init__(self, user_table, faq_table):
        self.user_table = user_table
        self.faq_table = faq_table
    
    def getFaqByDepartment(self, department: str):
        faq = self.faq_table.query.filter_by(department = department).all()
        return faq
    
    def getFaqQuestionsByDepartment(self, department: str):
        faq_list = self.faq_table.query.filter_by(department = department).all()
        questions: list
        for faq in faq_list:
            questions.append(faq.question)
        return faq
    
    def getFaqAnswersByDepartment(self, department: str):
        faq_list = self.faq_table.query.filter_by(department = department).all()
        questions: list
        for faq in faq_list:
            questions.append(faq.answer)
        return faq

    def addFaq(self, department: str, faq_create_request: FaqCreateRequest):
        faq = self.faq_table(
            department=faq_create_request.department,
            question=faq_create_request.question,
            answer=faq_create_request.answer)
        db.session.add(faq)
        db.session.commit()
        return faq
    
    """
    Parametre olarak bir data transfer object (dto) alırsak yönetim daha rahat olur
    Ayrıca response olarak da dto döndürülebilir ama iş yükü artmasın şimdilik
    """
    def updateFaq(self, id: int, faq_update_request: FaqUpdateRequest):
        faq = self.faq_table.query.filter_by(id=id).first()

        print("in updatefaq, req", faq_update_request.question, faq_update_request.answer)
        print("in updatefaq, faq", faq.question, faq.answer)
        faq.department = faq_update_request.department
        faq.question = faq_update_request.question
        faq.answer = faq_update_request.answer
        print("in updatefaq, faq", faq.question, faq.answer)
        # faq.date = datetime.datetime.now
        db.session.commit()
        return faq

    def deleteFaq(self, id: int):
        faq = self.faq_table.query.filter_by(id = id).first()
        db.session.delete(faq)
        db.session.commit()
    
    def getAllQuestions(self):
        all_data = self.faq_table.query.all()
        return all_data