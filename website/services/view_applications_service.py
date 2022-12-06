from website import db

class ViewApplicationsService():   
    def __init__(self, user_table):
        self.user_table = user_table