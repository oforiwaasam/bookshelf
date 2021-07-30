# login_manager.py
#
# Will hold functions that are in charge of handling the user
# login and registration system, so the users information is 
# stored correctly 
# 

    
# Saves the value of the logged in user. 
# Uses the User class as inputs to log people in
class Login_Manager():
    def __init__(self):
        self.user = None #default not logged in
    
    # Login user by setting it to current user
    def login(self, user):
        self.user = user

    # Logout user by setting user to None
    def logout(self, user):
        self.user = None
    
    def is_logged_in(self):
        if self.user is None:
            return False
        return True
    
    def get_username(self):
        if not self.is_logged_in():
            return ""
        return self.user.username
    
    def get_email(self):
        if not self.is_logged_in():
            return ""
        return self.user.email
    
    def __str__(self):
        if self.is_logged_in():
            return f'Currently {self.user.username} is logged in'  
        else:
            return 'Nobody is currently logged in'
