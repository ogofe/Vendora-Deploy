from django.shortcuts import redirect



def has_password(request, store_name, fun):
    if not request.user.has_usable_password():
        return redirect('accounts:store-login', store_name)
    return fun()