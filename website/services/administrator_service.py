from website import db
from website.models import user

class AdministratorService():   
    def __init__(self, user_table):
        self.user_table = user_table