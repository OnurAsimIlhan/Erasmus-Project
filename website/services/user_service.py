from website import db
from website.models import User

class UserService():
    def __init__(self, user_table):
        self.user_table = user_table
    
    
    def getUserById(self, id: int):
        user: User = self.user_table.query.filter_by(bilkent_id = id).first()
        return user