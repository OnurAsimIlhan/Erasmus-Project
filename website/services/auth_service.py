class AuthService():
    def __init__(self, user_table, role_table):
        self.user_table = user_table
        self.role_table = role_table
    
    def authenticate(self, bilkent_id: int, password: str):
        user = self.user_table.query.filter_by(bilkent_id=bilkent_id).first()
        
        if (user == None) or (password != user.password):
            return False, False 
        else:
            role = self.role_table.query.filter_by(user_id=bilkent_id).all()
            return user, role

    def authoriza(self, user):
        # To be Continued...
        pass
    