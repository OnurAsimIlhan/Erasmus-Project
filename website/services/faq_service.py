import datetime
from website import db
from website.dtos.faqUpdateRequest import FaqUpdateRequest
from website.models import Faq

class FaqService():
    def __init__(self, user_table, faq_table):
        self.user_table = user_table
        self.faq_table = faq_table
    
    def getFaqByDepartment(self, department: str):
        faq = self.faq_table.query.filter_by(department = department).first()
        return faq

    """Şimdilik pas geçelim """
    def addFaq():
        pass
    
    """
    Parametre olarak bir data transfer object (dto) alırsak yönetim daha rahat olur
    Ayrıca response olarak da dto döndürülebilir ama iş yükü artmasın şimdilik
    """
    def updateFaq(self, department: str, faq_update_request: FaqUpdateRequest):
        faq:Faq = self.faq_table.query.filter_by(department=department).first()
        faq.info = faq_update_request.info
        faq.department = faq_update_request.department
        # faq.date = datetime.datetime.now
        db.session.commit()
        return faq