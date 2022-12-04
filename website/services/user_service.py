class UserService():
    def __init__(self, user_table):
        self.user_table = user_table

    def getAllUsers(self):
        contacts_list = self.user_table.query.all()
        return contacts_list
    