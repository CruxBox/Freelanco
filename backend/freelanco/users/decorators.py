from functools import wraps
from django.core.exceptions import PermissionDenied

def only_customer(func):
    @wraps(func)
    def inner_func(request,*args,**kwargs):
        if request.user.is_freelancer:
            raise PermissionDenied
        else:
            return func(request,*args,**kwargs)
    return inner_func

def only_freelancer(func):
    @wraps(func)
    def inner_func(request,*args,**kwargs):
        if not request.user.is_freelancer:
            raise PermissionDenied
        else:
            return func(request,*args,**kwargs)
    return inner_func