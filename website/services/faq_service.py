class FaqService():
    def __init__(self, faq_t):
        self.faq_t = faq_t
        

    def getAllQuestions(self):
        all_data = self.faq_t.query.all()
        return all_data
    
   