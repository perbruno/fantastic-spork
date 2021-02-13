from .models import User

class Watchlist:
    def __init__(self,email):
        self.email = email

    def validate_user(self):
        user_data = User.objects.filter(email__exact=self.email).values()
        if len(user_data)!=1:
            raise ValueError("User {} doesn't exist.".format(self.email))
        return user_data
        

    def get_watchlist(self):
        user_data = self.validate_user()
        watchlist = user_data.first().get('watchlist')
        return watchlist if watchlist!='{}' else "User's watchlist is empty"
        
    
    def post_watchlist(self,**kwargs):
        """
        the following model must be respected:
            user.post_watchlist(code = {'buy': 00.00 , 'sell':10.00} ...)
        """ 
        self.validate_user()

    
    def put_watchlist(self,**kwargs):
        """
        the following model must be respected:
            user.put_watchlist(code = {'buy': 00.00 , 'sell':10.00} ...)
        """
        self.validate_user()
        pass


    def delete_watchlist(self, **kwargs):
        self.validate_user()
        pass