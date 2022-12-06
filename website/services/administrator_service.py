from website import db

class AdministratorService():   
    def __init__(self, user_table):
        self.user_table = user_table