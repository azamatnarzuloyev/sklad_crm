from django.contrib.auth import get_user_model
from account.models import User

def run():
    user = User()
    user.phone = "998990161111"
    user.save()
    print(user)
    
    

