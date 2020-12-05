from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import BasePermission
from store.models import Store

# re = requests.Request(get, 'ddd', {})
# re.url
# re = requests

class Is_Merchant(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            try:
                if request.user.merchant:
                    if obj.store.owner == request.user.merchant:
                        return True
                    return False
            except:
                return False
        return False
    
    
     
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                if request.user.merchant:
                    return True
            except:
                return False
        return False


class Is_Merchant_or_Staff(BasePermission):
    def has_object_permission(self, request, view, obj, **kwargs):
        store = Store.objects.get(slug=view.kwargs['slug'])        
        if request.user in store.staff_accounts.all():
            return True
        return False
    
    
     
    def has_permission(self, request, view, **kwargs):
        store = Store.objects.get(slug=view.kwargs['slug'])        
        if request.user in store.staff_accounts.all():
            return True
        return False
    
    

