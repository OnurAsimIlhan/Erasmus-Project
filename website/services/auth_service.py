class AuthService():
    def __init__(self, user_table, role_table):
        self.user_table = user_table
        self.role_table = role_table
    
    def authenticate(self, bilkent_id: int, password: str):
        """ Only used in the Login Page """
        user = self.user_table.query.filter_by(bilkent_id=bilkent_id).first()
        
        if (user == None) or (password != user.password):
            return False, False 
        else:
            role = self.role_table.query.filter_by(bilkent_id=bilkent_id).all()
            return user, role

    def is_authorized(self, user, required_role: str):
        """ 
            from flask_login import login_required, current_user, logout_user
        
            @app.route("/example_route")
            @login_required
            def example_route_function():
                if auth_service.is_authorized(user=current_user, required_role="student"):
                    ...
                    ...
                else:
                    logout_user()
                    return redirect(url_for("your_are_not_authorized_page"))  
        """
        
        user_role = self.role_table.query.filter_by(bilkent_id=user.bilkent_id).all()
        user_role = [role.role for role in user_role]
        
        if required_role in user_role:
            return True
        else:
            return False