from django.conf import settings
from django.contrib.auth.hashers import check_password
from store.models import Store


# a custom backend to authenticate emails
class StoreLoginBackend:
    """
    Authenticate against Store Name and Password.
    
    """

    def authenticate(self, request, username=None, password=None):
        login_valid = (request.POST['username'] == username)
        pwd_valid = check_password(password, request.POST['password'])
        try:
            email = Store.objects.get(name=request.POST['username']).owner
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None

    def get_store(self, store_name):
        try:
            return Store.objects.get(name=store_name)
        except Store.DoesNotExist:
            return None
                